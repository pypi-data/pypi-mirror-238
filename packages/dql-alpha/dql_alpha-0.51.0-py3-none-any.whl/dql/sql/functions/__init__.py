from sqlalchemy.sql.expression import func

from . import path  # noqa: F401

count = func.count
sum = func.sum  # pylint: disable=redefined-builtin
avg = func.avg
min = func.min  # pylint: disable=redefined-builtin
max = func.max  # pylint: disable=redefined-builtin
