from datetime import datetime, timedelta
from operator import eq
from typing import Callable, Any, Tuple, Mapping, Optional

from pyannotating import Special

from act.annotations import V, dirty, reformer_of, ActionT, K
from act.representations import ActionReprMixnin


__all__ = (
    "documenting_by",
    "to_check",
    "as_action",
    "time_of",
    "items_of",
    "maybe_getattr",
    "maybe_getitem",
)


class Decorator(ActionReprMixnin):
    """
    Abstract class for decorating an input action and creating a signature
    based on it.

    Set signature from `_force_signature` attribute.

    When `_doc_parser = True` assigns itself an input action documentation.
    """

    def __init__(self, action: ActionT):
        self._action = action


def documenting_by(documentation: str) -> dirty[reformer_of[V]]:
    """
    Function of getting other function that getting value with the input
    documentation from this first function.
    """

    def document(object_: V) -> V:
        """
        Function created with `documenting_by` function that sets the __doc__
        attribute and returns the input object.
        """

        object_.__doc__ = documentation
        return object_

    return document


def _get(value: V) -> V:
    """
    Function representing the absence of an action.
    Returns the value passed to it back.
    """

    return value


def to_check(determinant: Callable[V, bool] | V) -> Callable[V, bool]:
    """Function representing an input value to a validation action."""

    from act.flags import _CallableNamedFlag
    from act.partiality import partial

    return (
        determinant
        if callable(determinant) and not isinstance(determinant, _CallableNamedFlag)
        else partial(eq, determinant)
    )


def as_action(value: ActionT | V) -> ActionT | Callable[..., V]:
    """Function representing an input value to aт action."""

    return value if callable(value) else lambda *_, **__: value


def time_of(action: Callable[[], Any]) -> timedelta:
    """Function to get run time measurement of an input action."""

    start = datetime.now()
    action()

    return datetime.now() - start


def items_of(items: V | Tuple[V]) -> Tuple[V]:
    """Function for structured getting inside indexer (`[]`)."""

    return items if isinstance(items, tuple) else (items, )


def maybe_getattr(object_: Any, attr_name: str) -> Special[None]:
    return getattr(object_, attr_name) if hasattr(object_, attr_name) else None


def maybe_getitem(table: Mapping[K, V], key: Special[K]) -> Optional[V]:
    return table[key] if key in tuple(table.keys()) else None


def _module_prefix_of(action: Callable) -> str:
    prefix = str() if action.__module__ is None else action.__module__

    return str() if prefix in ("__main__", "builtins") else prefix + '.'
