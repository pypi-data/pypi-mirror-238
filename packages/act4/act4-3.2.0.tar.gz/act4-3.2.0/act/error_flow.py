from typing import Callable, Optional, Type, NoReturn

from act.annotations import Pm, R, ErrorT
from act.atomization import fun
from act.contexting import contextual
from act.data_flow import by, to, always
from act.partiality import partially
from act.pipeline import bind_by, then
from act.synonyms import try_, raise_
from act.tools import documenting_by


__all__ = (
    "with_error",
    "catch",
    "raising",
)


with_error: Callable[
    [Callable[Pm, R]],
    Callable[Pm, contextual[Optional[Exception], Optional[R]]]
]
with_error = documenting_by(
    """
    Decorator that causes the decorated function to return the error that
    occurred.

    Returns in `contextual` format (error, result).
    """
)(
    fun(
        bind_by(... |then>> contextual)
        |then>> (try_ |by| to(contextual |by| None))
    )
)


@partially
def catch(
    error_type_to_catch: Type[ErrorT],
    action: Callable[ErrorT, R],
    error: ErrorT,
) -> R:
    """
    Function to optionally handle an input error depending on its type.

    Throws an input error if an input error type does not match the expected
    type.
    """

    if not isinstance(error, error_type_to_catch):
        raise error

    return action(error)


raising: Callable[Exception, Callable[..., NoReturn]]
raising = documenting_by(
    """
    Constructor of an action that raises an input error ignoring input
    arguments.
    """
)(
    always |to| raise_
)
