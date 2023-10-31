"""Log error with decorator-function."""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, ParamSpec, TypeVar

if TYPE_CHECKING:
    import logging

P = ParamSpec("P")
T = TypeVar("T")


def error_exception(
    logger: logging.Logger,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Log error - outer function taking logger as an argument."""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        """Decorate the incoming function."""

        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            """Log possible error with wrapper-function."""
            try:
                return func(*args, **kwargs)
            except:
                err: str = f"An error occurred in {func.__name__}"
                logger.exception(err)

                raise

        return wrapper

    return decorator
