import pendulum
from pendulum.datetime import DateTime

__all__ = ["parse_dt", "now"]


def parse_dt(dt: str, **options) -> DateTime:
    """Parse `dt` and return a datetime object."""
    return pendulum.parser.parse(dt, **options)


def now() -> DateTime:
    """Return the current datetime."""
    return pendulum.now("UTC")
