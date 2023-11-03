import contextlib
import os
import random
import string
import subprocess  # nosec B404
import sys
from abc import ABC, abstractmethod
from copy import copy
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

import attrs
import sqlalchemy
from attrs import frozen
from dill import dumps  # nosec B403
from sqlalchemy.sql import func as f
from sqlalchemy.sql.expression import label

from dql.catalog import QUERY_SCRIPT_INVALID_LAST_STATEMENT_EXIT_CODE, get_catalog
from dql.data_storage.schema import (
    DATASET_CORE_COLUMN_NAMES,
    PARTITION_COLUMN_ID,
    PARTITION_COLUMN_SIZE,
    PARTITION_UNIQUE_ID,
)
from dql.data_storage.schema import DatasetRow as DatasetRowSchema
from dql.data_storage.schema import partition_col_names, partition_columns
from dql.dataset import Status as DatasetStatus
from dql.utils import chunk, flatten

from .batch import NoBatching, Partition
from .schema import C
from .udf import UDFClassWrapper, UDFFactory, UDFType

if TYPE_CHECKING:
    from sqlalchemy.sql.elements import ColumnElement
    from sqlalchemy.sql.schema import Table
    from sqlalchemy.sql.selectable import SelectBase

    from dql.catalog import Catalog


INSERT_BATCH_SIZE = 10000

GroupByType = Union["ColumnElement", Sequence["ColumnElement"]]


class QueryGeneratorFunc(Protocol):
    def __call__(self, *columns: "ColumnElement") -> "SelectBase":
        ...


@frozen
class QueryGenerator:
    func: QueryGeneratorFunc
    columns: Tuple["ColumnElement", ...]

    def exclude(self, column_names) -> "SelectBase":
        return self.func(*[c for c in self.columns if c.name not in column_names])

    def select(self, column_names=None) -> "SelectBase":
        if column_names is None:
            return self.func(*self.columns)
        return self.func(*[c for c in self.columns if c.name in column_names])


@frozen
class StepResult:
    query_generator: QueryGenerator
    temp_table_names: Tuple[str, ...]


def step_result(
    func: QueryGeneratorFunc,
    columns: Iterable["ColumnElement"],
    temp_table_names: Iterable[str] = (),
) -> "StepResult":
    return StepResult(
        query_generator=QueryGenerator(func=func, columns=tuple(columns)),
        temp_table_names=tuple(temp_table_names),
    )


class StartingStep(ABC):
    """An initial query processing step, referencing a data source."""

    @abstractmethod
    def apply(self) -> "StepResult":
        ...


@frozen
class Step(ABC):
    """A query processing step (filtering, mutation, etc.)"""

    @abstractmethod
    def apply(self, query_generator: "QueryGenerator") -> "StepResult":
        """Apply the processing step."""


@frozen
class QueryStep(StartingStep):
    table: "Table"

    def apply(self):
        """Return the query for the table the query refers to."""
        table = self.table

        def q(*columns):
            return sqlalchemy.select(*columns)

        return step_result(q, table.c)


@frozen
class IndexingStep(StartingStep):
    path: str
    catalog: "Catalog"
    kwargs: Dict[str, Any]

    def apply(self):
        """Return the query for the table the query refers to."""
        # TODO return data_storages from this index() call and use them below
        self.catalog.index([self.path], **self.kwargs)
        uri, path = self.parse_path()

        partial_id = self.catalog.data_storage.get_valid_partial_id(uri, path)
        st = self.catalog.data_storage.clone(uri, partial_id)

        def q(*columns):
            col_names = [c.name for c in columns]
            return st.nodes_dataset_query(
                column_names=col_names, path=path, recursive=True, uri=uri
            )

        dataset_columns = DatasetRowSchema.calculate_all_columns([st.nodes])
        return step_result(q, dataset_columns)

    def parse_path(self):
        client_config = self.kwargs.get("client_config") or {}
        client, path = self.catalog.parse_url(self.path, **client_config)
        return client.uri, path


def generator_then_call(generator, func: Callable):
    """
    Yield items from generator then execute a function and yield
    its result.
    """
    yield from generator
    yield func() or []


class DatasetDiffOperation(Step):
    """
    Abstract class for operations that are calculation some kind of diff between
    datasets queries like subtract, changed etc.
    """

    dq: "DatasetQuery"
    catalog: "Catalog"

    def clone(self):
        return self.__class__(self.dq, self.catalog)

    @abstractmethod
    def query(
        self,
        source_query: sqlalchemy.sql.selectable.Select,
        target_query: sqlalchemy.sql.selectable.Select,
    ) -> sqlalchemy.sql.selectable.Select:
        """
        Should return select query that calculates desired diff between dataset queries
        """

    def apply(self, query_generator):
        source_query = query_generator.exclude(("id", "parent_id"))
        target_query = self.dq.apply_steps().select()

        # creating temp table that will hold subtract results
        temp_table_name = "tmp_" + _random_string(6)
        custom_columns = [
            sqlalchemy.Column(col.name, col.type)
            for col in source_query.columns
            if col.name not in DATASET_CORE_COLUMN_NAMES
        ]
        temp_table = self.catalog.data_storage.create_dataset_rows_table(
            temp_table_name,
            custom_columns=custom_columns,
            if_not_exists=False,
        )

        diff_q = self.query(source_query, target_query)

        insert_q = temp_table.insert().from_select(
            source_query.selected_columns, diff_q
        )

        self.catalog.data_storage.ddb.execute(insert_q)

        def q(*columns):
            return sqlalchemy.select(*columns).select_from(temp_table)

        return step_result(q, temp_table.c, temp_table_names=[temp_table.name])


@frozen
class Subtract(DatasetDiffOperation):
    """
    Calculates rows that are in a source query but are not in target query (diff)
    This can be used to do delta updates (calculate UDF only on newly added rows)
    Example:
        >>> ds = DatasetQuery(name="dogs_cats") # some older dataset with embeddings
        >>> ds_updated = (
                DatasetQuery("s3://ldb-public/remote/data-lakes/dogs-and-cats")
                .filter(C.size > 1000) # we can also filter out source query
                .subtract(ds)
                .add_signals(calc_embeddings) # calculae embeddings only on new rows
                .union(ds) # union with old dataset that's missing new rows
                .save("dogs_cats_updated")
            )
    """

    dq: "DatasetQuery"
    catalog: "Catalog"

    def query(self, source_query, target_query) -> sqlalchemy.sql.selectable.Select:
        return self.catalog.data_storage.subtract_query(source_query, target_query)


@frozen
class Changed(DatasetDiffOperation):
    """
    Calculates rows that are changed in a source query compared to target query
    Changed means it has same source + parent + name but different last_modified
    Example:
        >>> ds = DatasetQuery(name="dogs_cats") # some older dataset with embeddings
        >>> ds_updated = (
                DatasetQuery("s3://ldb-public/remote/data-lakes/dogs-and-cats")
                .filter(C.size > 1000) # we can also filter out source query
                .changed(ds)
                .add_signals(calc_embeddings) # calculae embeddings only on changed rows
                .union(ds) # union with old dataset that's missing updated rows
                .save("dogs_cats_updated")
            )

    """

    dq: "DatasetQuery"
    catalog: "Catalog"

    def query(self, source_query, target_query) -> sqlalchemy.sql.selectable.Select:
        return self.catalog.data_storage.changed_query(source_query, target_query)


@frozen
class UDF(Step, ABC):
    udf: UDFType
    catalog: "Catalog"
    group_by: Optional[GroupByType] = None
    processes: Union[bool, int] = False
    workers: Union[bool, int] = False
    min_task_size: Optional[int] = None
    is_generator = False

    @abstractmethod
    def create_udf_table(self, query, udf) -> "Table":
        """Method that creates a table where temp udf results will be saved"""

    @abstractmethod
    def create_result_query(
        self, udf_table, query
    ) -> Tuple[QueryGeneratorFunc, List["sqlalchemy.Column"]]:
        """
        Method that should return query to fetch results from udf and columns
        to select
        """

    def udf_table_name(self) -> str:
        return "udf_" + _random_string(6)

    @staticmethod
    def add_defaults(rows: List[Dict[str, Any]], udf) -> None:
        """
        Fill default values for columns that have None values and add missing ones
        """
        udf_outputs = {col_name: col_type for (col_name, col_type) in udf.output}

        for row in rows:
            empty_row_cols = [
                row_col for row_col, row_val in row.items() if row_val is None
            ]
            # convert None values to empty values for specific type
            for empty_col in empty_row_cols:
                row[empty_col] = udf_outputs[empty_col].default_value()

            # fill out missing columns that should exist according to udf output
            for col_name, col_type in udf_outputs.items():
                if col_name not in row:
                    row[col_name] = col_type.default_value()

    def populate_udf_table(self, udf_table, query, udf) -> None:
        with_group_by = self.group_by is not None

        # Some udfs may be defined without the @udf decorator.
        if hasattr(udf, "properties"):
            batching = udf.properties.get_batching(with_group_by)
        elif with_group_by:
            batching = Partition()
        else:
            batching = NoBatching()

        try:
            if self.workers:
                from dql.catalog.loader import get_distributed_class

                distributor = get_distributed_class(min_task_size=self.min_task_size)
                distributor(
                    udf,
                    self.catalog,
                    udf_table,
                    query,
                    self.workers,
                    self.processes,
                    is_generator=self.is_generator,
                )
            elif self.processes:
                # Parallel processing (faster for more CPU-heavy UDFs)
                udf_info = {
                    "udf": udf,
                    "catalog_init": self.catalog.get_init_params(),
                    "data_storage_params": self.catalog.data_storage.clone_params(),
                    "table": udf_table,
                    "query": query,
                    "batching": batching,
                    "processes": self.processes,
                    "is_generator": self.is_generator,
                }
                process_data = dumps(udf_info, recurse=True)
                # Run the UDFDispatcher in another process to avoid needing
                # if __name__ == '__main__': in user scripts
                dql_exec_path = os.environ.get("DQL_EXEC_PATH", "dql")
                # pylint: disable=W1510
                result = subprocess.run(  # nosec B603
                    [dql_exec_path, "--internal-run-udf"],
                    input=process_data,
                )
                if result.returncode != 0:
                    raise RuntimeError("UDF Execution Failed!")
            else:
                # Otherwise process single-threaded (faster for smaller UDFs)
                # Optionally instantiate the UDF instance if a class is provided.
                if isinstance(udf, UDFFactory):
                    udf = udf()

                udf_inputs = batching(
                    self.catalog.data_storage.dataset_select_paginated, query
                )
                udf_results = (
                    udf(self.catalog, row, output_rows=self.is_generator)
                    for row in udf_inputs
                )

                rows = []
                for udf_output in udf_results:
                    if not udf_output:
                        continue
                    # we need to flatten as we can get multiple results for one
                    # row (e.g in generators)
                    new_rows = list(flatten(udf_output))
                    self.add_defaults(new_rows, udf)
                    rows.extend(new_rows)
                    if len(rows) > INSERT_BATCH_SIZE:
                        for row_chunk in chunk(rows, INSERT_BATCH_SIZE):
                            self.catalog.data_storage.insert_rows(udf_table, row_chunk)
                        rows.clear()
                if rows:
                    for row_chunk in chunk(rows, INSERT_BATCH_SIZE):
                        self.catalog.data_storage.insert_rows(udf_table, row_chunk)
                self.catalog.data_storage.insert_rows_done(udf_table)
        except Exception:
            # Close any open database connections if an error is encountered
            self.catalog.data_storage.close()
            raise

    def create_partitions_table(self, query) -> "Table":
        """
        Create temporary table with group by partitions.
        """
        group_by = self.group_by
        if not isinstance(group_by, Sequence):
            group_by = [group_by]

        id_col = next(c for c in query.selected_columns if c.name == "id")

        # create table with partitions
        tbl = self.catalog.data_storage.create_udf_table(
            self.udf_table_name(),
            id_col.type,
            partition_columns(),
        )

        # fill table with partitions
        cols = [
            id_col,
            f.dense_rank().over(order_by=group_by).label(PARTITION_COLUMN_ID),
            f.count().over(partition_by=group_by).label(PARTITION_COLUMN_SIZE),
            label(PARTITION_UNIQUE_ID, 0),
        ]
        self.catalog.data_storage.ddb.execute(
            tbl.insert().from_select(cols, query.with_only_columns(cols))
        )
        self.catalog.data_storage.update_partition_unique_id(tbl)

        return tbl

    def clone(self, group_by: Optional[GroupByType] = None):
        if group_by is not None:
            return self.__class__(
                self.udf,
                self.catalog,
                group_by=group_by,
                processes=self.processes,
                workers=self.workers,
                min_task_size=self.min_task_size,
            )
        return self.__class__(self.udf, self.catalog)

    def apply(self, query_generator):  # noqa: C901
        query = query_generator.select()
        temp_tables = []

        # Apply partitioning if needed.
        if self.group_by is not None:
            partition_tbl = self.create_partitions_table(query)
            temp_tables.append(partition_tbl.name)

            subq = query.subquery()
            query = (
                sqlalchemy.select(*subq.c)
                .select_from(subq)
                .outerjoin(partition_tbl, partition_tbl.c.id == subq.c.id)
                .add_columns(*partition_columns())
            )

        if isinstance(self.udf, UDFClassWrapper):
            udf = self.udf()
        else:
            udf = self.udf

        udf_table = self.create_udf_table(query, udf)
        temp_tables.append(udf_table.name)
        self.populate_udf_table(udf_table, query, udf)
        q, cols = self.create_result_query(udf_table, query)

        return step_result(q, cols, temp_table_names=temp_tables)


@frozen
class UDFSignal(UDF):
    udf: UDFType
    catalog: "Catalog"
    group_by: Optional[GroupByType] = None
    processes: Union[bool, int] = False
    workers: Union[bool, int] = False
    min_task_size: Optional[int] = None
    is_generator = False

    def create_udf_table(self, query, udf) -> "Table":
        id_col = next(c for c in query.selected_columns if c.name == "id")
        udf_output_columns = [
            sqlalchemy.Column(col_name, col_type) for (col_name, col_type) in udf.output
        ]

        return self.catalog.data_storage.create_udf_table(
            self.udf_table_name(),
            id_col.type,
            udf_output_columns,
        )

    def create_result_query(
        self, udf_table, query
    ) -> Tuple[QueryGeneratorFunc, List["sqlalchemy.Column"]]:
        subq = query.subquery()
        original_cols = [c for c in subq.c if c.name not in partition_col_names]

        # new signal columns that are added to udf_table
        signal_cols = [c for c in udf_table.c if c.name != "id"]
        signal_name_cols = {c.name: c for c in signal_cols}
        cols = signal_cols

        def q(*columns):
            cols1 = []
            cols2 = []
            for c in columns:
                if c.name in partition_col_names:
                    continue
                cols.append(signal_name_cols.get(c.name, c))
                if c.name in signal_name_cols.keys():
                    cols2.append(c)
                else:
                    cols1.append(c)

            if cols2:
                res = (
                    sqlalchemy.select(*cols1)
                    .select_from(subq)
                    .join(udf_table, udf_table.c.id == subq.c.id)
                    .add_columns(*cols2)
                )
            else:
                res = sqlalchemy.select(*cols1).select_from(subq)

            if self.group_by is not None:
                subquery = res.subquery()
                res = sqlalchemy.select(*subquery.c).select_from(subquery)

            return res

        return q, [*original_cols, *cols]


@frozen
class RowGenerator(UDF):
    """Extend dataset with new rows."""

    udf: UDFType
    catalog: "Catalog"
    group_by: Optional[GroupByType] = None
    processes: Union[bool, int] = False
    workers: Union[bool, int] = False
    min_task_size: Optional[int] = None
    is_generator = True

    def create_udf_table(self, query, udf) -> "Table":
        table_name = self.udf_table_name()
        if isinstance(udf, UDFFactory):
            udf = udf()

        custom_columns: List["sqlalchemy.Column"] = [
            sqlalchemy.Column(col.name, col.type)
            for col in query.selected_columns
            if col.name not in DATASET_CORE_COLUMN_NAMES
        ]
        custom_column_names = tuple([c.name for c in custom_columns])

        custom_udf_output_columns = [
            sqlalchemy.Column(col_name, col_type)
            for (col_name, col_type) in udf.output
            if col_name not in DATASET_CORE_COLUMN_NAMES + custom_column_names
        ]

        self.catalog.data_storage.create_dataset_rows_table(
            table_name,
            custom_columns=custom_columns + custom_udf_output_columns,
            if_not_exists=False,
        )
        udf_table = self.catalog.data_storage.get_table(table_name)

        return udf_table

    def create_result_query(
        self, udf_table, query
    ) -> Tuple[QueryGeneratorFunc, List["sqlalchemy.Column"]]:
        # pylint: disable=W0212
        if query._limit and not query._order_by_clauses:
            # if we are not selecting all rows in UDF, we need to ensure that
            # we get the same rows as we got as inputs of UDF since selecting
            # without ordering can be non deterministic in some databases
            query = query.order_by(query.selected_columns.id)
        original_query = query.subquery()
        original_cols = [
            label(c.name, c)
            for c in original_query.columns
            if c.name not in partition_col_names
        ]
        original_col_names = {c.name for c in original_cols}

        udf_table_query = udf_table.select().subquery()
        udf_table_cols = [label(c.name, c) for c in udf_table_query.columns]

        newly_created_cols = [
            label(c.name, c)
            for c in udf_table_query.columns
            if c.name not in original_col_names
        ]

        def q(*columns):
            names = {c.name for c in columns}
            cols1 = [c for c in original_cols if c.name in names]
            cols2 = [
                c for c in udf_table_cols if c.name in names
            ]  # Columns for the generated table.

            if newly_created_cols:
                # in order for union to work, it must have the same amount
                # of columns in both subqueries, so filling out missing ones
                for c in newly_created_cols:
                    if c.name in partition_col_names:
                        continue
                    default_value = None
                    if self.catalog.data_storage.python_type(c.type) == list:
                        default_value = []
                    cols1.append(sqlalchemy.literal(default_value).label(c.name))

            res = sqlalchemy.union_all(
                sqlalchemy.select(*cols1).select_from(original_query),
                sqlalchemy.select(*cols2).select_from(udf_table_query),
            )

            subquery = res.subquery()
            return sqlalchemy.select(*subquery.c).select_from(subquery)

        return q, [*original_cols] + [*newly_created_cols]


@frozen
class SQLClause(Step, ABC):
    def apply(self, query_generator):
        query = query_generator.select()
        new_query = self.apply_sql_clause(query)

        def q(*columns):
            return new_query.with_only_columns(*columns)

        return step_result(q, new_query.selected_columns)

    @abstractmethod
    def apply_sql_clause(self, query):
        pass


@frozen
class SQLSelect(SQLClause):
    args: Tuple["ColumnElement", ...]

    def apply_sql_clause(self, query):
        subquery = query.subquery()
        args = [subquery.c[c] if isinstance(c, str) else c for c in self.args]
        if not args:
            args = subquery.c
        return sqlalchemy.select(*args).select_from(subquery)


@frozen
class SQLSelectExcept(SQLClause):
    args: Tuple[str, ...]

    def apply_sql_clause(self, query):
        subquery = query.subquery()
        names = set(self.args)
        args = [c for c in subquery.c if c.name not in names]
        return sqlalchemy.select(*args).select_from(subquery)


@frozen
class SQLMutate(SQLClause):
    args: Tuple["ColumnElement", ...]

    def apply_sql_clause(self, query):
        subquery = query.subquery()
        return sqlalchemy.select(*subquery.c, *self.args).select_from(subquery)


@frozen
class SQLFilter(SQLClause):
    expressions: Tuple["ColumnElement", ...]

    def __and__(self, other):
        return self.__class__(self.expressions + other)

    def apply_sql_clause(self, query):
        return query.filter(*self.expressions)


@frozen
class SQLOrderBy(SQLClause):
    args: Tuple["ColumnElement", ...]

    def apply_sql_clause(self, query):
        return query.order_by(*self.args)


@frozen
class SQLLimit(SQLClause):
    n: int

    def apply_sql_clause(self, query):
        return query.limit(self.n)


@frozen
class SQLCount(SQLClause):
    def apply_sql_clause(self, query):
        return sqlalchemy.select(f.count(1)).select_from(query.subquery())


@frozen
class SQLUnion(Step):
    query1: "SQLQuery"
    query2: "SQLQuery"

    def apply(self, query_generator):
        q1 = self.query1.apply_steps().select().subquery()
        q2 = self.query2.apply_steps().select().subquery()
        columns1, columns2 = fill_columns(q1.columns, q2.columns)

        def q(*columns):
            names = {c.name for c in columns}
            col1 = [c for c in columns1 if c.name in names]
            col2 = [c for c in columns2 if c.name in names]
            res = (
                sqlalchemy.select(*col1)
                .select_from(q1)
                .union_all(sqlalchemy.select(*col2).select_from(q2))
            )

            subquery = res.subquery()
            return sqlalchemy.select(*subquery.c).select_from(subquery)

        return step_result(q, columns1)


@frozen
class GroupBy(Step):
    """Group rows by a specific column."""

    cols: GroupByType

    def clone(self):
        return self.__class__(self.cols)

    def apply(self, query_generator):
        query = query_generator.select()
        grouped_query = query.group_by(*self.cols)

        def q(*columns):
            return grouped_query.with_only_columns(*columns)

        return step_result(q, grouped_query.selected_columns)


def fill_columns(
    *column_iterables: Iterable["ColumnElement"],
) -> List[List["ColumnElement"]]:
    column_dicts = [{c.name: c for c in columns} for columns in column_iterables]
    combined_columns = {n: c for col_dict in column_dicts for n, c in col_dict.items()}

    result: List[List["ColumnElement"]] = [[] for _ in column_dicts]
    for n in combined_columns:
        col = next(col_dict[n] for col_dict in column_dicts if n in col_dict)
        for col_dict, out in zip(column_dicts, result):
            if n in col_dict:
                out.append(col_dict[n])
            else:
                # Cast the NULL to ensure all columns are aware of their type
                # Label it to ensure it's aware of its name
                out.append(sqlalchemy.cast(sqlalchemy.null(), col.type).label(n))
    return result


@attrs.define
class ResultIter:
    _row_iter: Iterable[Any]
    columns: List[str]

    def __iter__(self):
        yield from self._row_iter


SQLQueryT = TypeVar("SQLQueryT", bound="SQLQuery")


class SQLQuery:
    def __init__(
        self,
        starting_step: StartingStep,
        steps: Optional[Iterable["Step"]] = None,
        catalog: Optional["Catalog"] = None,
        client_config=None,
    ):  # pylint: disable=super-init-not-called
        self.steps: List["Step"] = list(steps) if steps is not None else []
        self.starting_step: StartingStep = starting_step
        self.catalog = catalog or get_catalog(client_config=client_config)
        self._chunk_index: Optional[int] = None
        self._chunk_total: Optional[int] = None
        self.temp_table_names: List[str] = []

    def __iter__(self):
        return iter(self.results())

    def __or__(self, other):
        return self.union(other)

    def apply_steps(self) -> QueryGenerator:
        """
        Apply the steps in the query and return the resulting
        sqlalchemy.SelectBase.
        """
        query = self.clone()

        index = os.getenv("DQL_QUERY_CHUNK_INDEX", self._chunk_index)
        total = os.getenv("DQL_QUERY_CHUNK_TOTAL", self._chunk_total)

        if index is not None and total is not None:
            index, total = int(index), int(total)  # os.getenv returns str

            if not (0 <= index < total):
                raise ValueError("chunk index must be between 0 and total")

            # Prepend the chunk filter to the step chain.
            query = query.filter(C.random % total == index)
            query.steps = query.steps[-1:] + query.steps[:-1]

        result = query.starting_step.apply()
        group_by = None
        self.temp_table_names.extend(result.temp_table_names)

        for step in query.steps:
            if isinstance(step, GroupBy):
                if group_by is not None:
                    raise TypeError("only one group_by allowed")
                group_by = step
                continue
            elif group_by is not None and isinstance(step, UDFSignal):
                if step.group_by is not None:
                    raise TypeError("only one group_by allowed")
                step = step.clone(group_by.cols)
                group_by = None

            result = step.apply(
                result.query_generator
            )  # a chain of steps linked by results
            self.temp_table_names.extend(result.temp_table_names)

        if group_by:
            result = group_by.apply(result.query_generator)
            self.temp_table_names.extend(result.temp_table_names)

        return result.query_generator

    def cleanup(self):
        self.catalog.data_storage.clone().cleanup_temp_tables(self.temp_table_names)
        self.temp_table_names = []

    def results(self, row_factory=None, **kwargs):
        with self.as_iterable(**kwargs) as result:
            if row_factory:
                cols = result.columns
                return [row_factory(cols, r) for r in result]
            else:
                return list(result)

    @contextlib.contextmanager
    def as_iterable(self, **kwargs) -> Iterator[ResultIter]:
        try:
            query = self.apply_steps()
            selected_columns = [c.name for c in query.columns]

            query = query.select()
            execute = self.catalog.data_storage.ddb.execute
            yield ResultIter(execute(query, **kwargs), selected_columns)
        finally:
            self.cleanup()

    def to_records(self):
        with self.as_iterable() as result:
            cols = result.columns
            return [dict(zip(cols, row)) for row in result]

    def to_pandas(self):
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "Missing required dependency pandas for DatasetQuery.to_pandas()\n"
                "To install run:\n\n"
                "  pip install 'dql-alpha[pandas]'\n"
            ) from exc

        records = self.to_records()
        df = pd.DataFrame.from_records(records)
        return df

    def clone(self: SQLQueryT) -> SQLQueryT:
        obj = copy(self)
        obj.steps = obj.steps.copy()
        return obj

    def select(self, *args, **kwargs):
        """
        Select the given columns or expressions using a subquery.

        If used with no arguments, this simply creates a subquery and
        select all columns from it.

        Note that the `save` function expects default dataset columns to
        be present. This function is meant to be followed by a call to
        `results` if used to exclude any default columns.

        Example:
            >>> ds.select(C.name, C.size * 10).results()
            >>> ds.select(C.name, size10x=C.size * 10).order_by(C.size10x).results()
        """
        named_args = [v.label(k) for k, v in kwargs.items()]
        query = self.clone()
        query.steps.append(SQLSelect((*args, *named_args)))
        return query

    def select_except(self, *args):
        """
        Exclude certain columns from this query using a subquery.

        Note that the `save` function expects default dataset columns to
        be present. This function is meant to be followed by a call to
        `results` if used to exclude any default columns.

        Example:
            >>> (
            ...     ds.mutate(size10x=C.size * 10)
            ...     .order_by(C.size10x)
            ...     .select_exclude(C.size10x)
            ...     .results()
            ... )
        """

        if not args:
            raise TypeError("select_except expected at least 1 argument, got 0")
        args = [c if isinstance(c, str) else c.name for c in args]
        query = self.clone()
        query.steps.append(SQLSelectExcept(args))
        return query

    def select_default(self):
        """
        Select only the default dataset columns using a subquery.

        This assumes that none of the default dataset columns have
        already been excluded from this query. This is useful if you've
        added columns with `mutate` or `select` calls for filtering but
        only want the default columns in the final output.

        Example:
            >>> (
            ...     ds.mutate(size10x=C.size * 10)
            ...     .order_by(C.size10x)
            ...     .select_default()
            ...     .results()
            ... )
        """
        query = self.clone()
        query.steps.append(SQLSelect((*DATASET_CORE_COLUMN_NAMES,)))
        return query

    def mutate(self, *args, **kwargs):
        """
        Add new columns to this query.

        This function selects all existing columns from this query and
        adds in the new columns specified.

        Example:
            >>> ds.mutate(size10x=C.size * 10).order_by(C.size10x).results()
        """
        args = [v.label(k) for k, v in dict(args, **kwargs).items()]
        query = self.clone()
        query.steps.append(SQLMutate((*args,)))
        return query

    def filter(self, *args):
        query = self.clone()
        steps = query.steps
        if steps and isinstance(steps[-1], SQLFilter):
            steps[-1] = steps[-1] & args
        else:
            steps.append(SQLFilter(args))
        return query

    def order_by(self, *args):
        query = self.clone()
        query.steps.append(SQLOrderBy(args))
        return query

    def limit(self, n: int):
        query = self.clone()
        query.steps.append(SQLLimit(n))
        return query

    def count(self):
        query = self.clone()
        query.steps.append(SQLCount())
        return query.results()[0][0]

    def sum(self, col: "ColumnElement"):
        query = self.clone()
        query.steps.append(SQLSelect((f.sum(col),)))
        return query.results()[0][0]

    def avg(self, col: "ColumnElement"):
        query = self.clone()
        query.steps.append(SQLSelect((f.avg(col),)))
        return query.results()[0][0]

    def min(self, col: "ColumnElement"):
        query = self.clone()
        query.steps.append(SQLSelect((f.min(col),)))
        return query.results()[0][0]

    def max(self, col: "ColumnElement"):
        query = self.clone()
        query.steps.append(SQLSelect((f.max(col),)))
        return query.results()[0][0]

    def group_by(self, *cols: "ColumnElement"):
        query = self.clone()
        query.steps.append(GroupBy(cols))
        return query

    def union(self, dataset_query):
        left = self.clone()
        right = dataset_query.clone()
        new_query = self.clone()
        new_query.steps = [SQLUnion(left, right)]
        return new_query

    def chunk(self, index: int, total: int):
        """Split a query into smaller chunks for e.g. parallelization.
        Example:
            >>> query = DatasetQuery(...)
            >>> chunk_1 = query._chunk(0, 2)
            >>> chunk_2 = query._chunk(1, 2)
        Note:
            Bear in mind that `index` is 0-indexed but `total` isn't.
            Use 0/3, 1/3 and 2/3, not 1/3, 2/3 and 3/3.
        """
        query = self.clone()
        query._chunk_index, query._chunk_total = index, total
        return query


class DatasetQuery(SQLQuery):
    def __init__(
        self,
        path: str = "",
        name: str = "",
        version: Optional[int] = None,
        catalog=None,
        client_config=None,
    ):
        if catalog is None:
            catalog = get_catalog(client_config=client_config)

        data_storage = catalog.data_storage
        starting_step: StartingStep
        if path:
            starting_step = IndexingStep(
                path, catalog, {"client_config": client_config}
            )
        elif name:
            ds = data_storage.get_dataset(name)
            version = version or ds.latest_version
            ds_table = catalog.data_storage.get_table(
                data_storage.dataset_table_name(ds.name, version=version)
            )
            starting_step = QueryStep(ds_table)
        else:
            raise ValueError("must provide path or name")

        super().__init__(
            starting_step=starting_step, catalog=catalog, client_config=client_config
        )

    def add_signals(
        self,
        udf: UDFType,
        processes: Union[bool, int] = False,
        workers: Union[bool, int] = False,
        min_task_size: Optional[int] = None,
        group_by: Optional[GroupByType] = None,
    ):
        """
        Adds one or more signals based on the results from the provided UDF.

        Processes can optionally be specified as >= 1 for parallel processing with a
        specific number of processes, or set to True for the default of
        the number of CPUs (cores) on the current machine.

        For distributed processing with the appropriate distributed module installed,
        workers can optionally be specified as >= 1 for a specific number of workers,
        or set to True for the default of all nodes in the cluster.
        As well, a custom minimum task size (min_task_size) can be provided to send
        at least that minimum number of rows to each distributed worker, mostly useful
        if there are a very large number of small tasks to process.
        """
        query = self.clone()
        query.steps.append(
            UDFSignal(
                udf,
                self.catalog,
                group_by=group_by,
                processes=processes,
                workers=workers,
                min_task_size=min_task_size,
            )
        )
        return query

    def subtract(self, dq: "DatasetQuery"):
        query = self.clone()
        query.steps.append(Subtract(dq, self.catalog))
        return query

    def changed(self, dq: "DatasetQuery"):
        query = self.clone()
        query.steps.append(Changed(dq, self.catalog))
        return query

    def generate(
        self,
        udf: UDFType,
        processes: Union[bool, int] = False,
        workers: Union[bool, int] = False,
        min_task_size: Optional[int] = None,
    ):
        query = self.clone()
        steps = query.steps
        steps.append(
            RowGenerator(
                udf,
                self.catalog,
                processes=processes,
                workers=workers,
                min_task_size=min_task_size,
            )
        )
        return query

    def save(self, name: str, **kwargs):
        """Save the query as a shadow dataset."""
        try:
            query = self.apply_steps()

            # Save to a temporary table first.
            temp_table_name = f"tmp_{name}_" + _random_string(6)
            custom_columns: List["sqlalchemy.Column"] = [
                sqlalchemy.Column(col.name, col.type)
                for col in query.columns
                if col.name not in DATASET_CORE_COLUMN_NAMES
            ]
            temp_table = self.catalog.data_storage.create_dataset_rows_table(
                temp_table_name,
                custom_columns=custom_columns,
                if_not_exists=False,
            )
            # Exclude the id column and let the db create it to avoid unique
            # constraint violations, and parent_id is not used in datasets.
            cols = [
                col.name for col in temp_table.c if col.name not in ("id", "parent_id")
            ]

            self.catalog.data_storage.ddb.execute(
                sqlalchemy.insert(temp_table).from_select(
                    cols, query.exclude(("id", "parent_id"))
                ),
                **kwargs,
            )

            # Create a shadow dataset.
            self.catalog.data_storage.create_shadow_dataset(name, create_rows=False)
            dataset = self.catalog.data_storage.get_dataset(name)
            if dataset is None:
                raise RuntimeError(f"No dataset found with {name=}")
            # pylint: disable=protected-access
            table_name = self.catalog.data_storage.dataset_table_name(dataset.name)

            self.catalog.data_storage._rename_table(temp_table_name, table_name)
            self.catalog.data_storage.update_dataset_status(
                dataset, DatasetStatus.COMPLETE
            )
        finally:
            self.cleanup()


def return_ds(dataset_query: DatasetQuery) -> DatasetQuery:
    """
    Wrapper function that wraps the last statement of user query script for creating
    shadow dataset (user sees it as query results in the UI).
    Last statement MUST be instance of DatasetQuery, otherwise script exits with
    error code 10
    """

    if not isinstance(dataset_query, DatasetQuery):
        sys.exit(QUERY_SCRIPT_INVALID_LAST_STATEMENT_EXIT_CODE)

    if isinstance(dataset_query, DatasetQuery):
        ds_id = _random_string(6)
        ds_name = f"ds_return_{ds_id}"
        dataset_query.catalog.data_storage.return_ds_hook(ds_name)
        dataset_query.save(ds_name)
    return dataset_query


def _random_string(length: int) -> str:
    return "".join(
        random.choice(string.ascii_letters + string.digits)  # nosec B311
        for i in range(length)
    )
