from typing import Callable, Generic, Optional, Self, Final, Any, Union, Tuple
from operator import attrgetter

from pyannotating import Special

from act.annotations import V, R, C, M, I, A, reformer_of
from act.atomization import fun
from act.pipeline import then
from act.contexting import contexted, contextual
from act.data_flow import by, yes
from act.operators import not_
from act.partiality import partial
from act.representations import code_like_repr_of
from act.synonyms import on
from act.tools import documenting_by, items_of, _get


__all__ = ("Effect", "as_effect", "context_effect")


class Effect(Generic[V, R, C]):
    """
    Aggregating decorator class for executing in a specific container type and
    actions for casting value to this container type.

    Aggregates an action of specifying a value as a container type (`is_lifted`),
    casting it to a container type (`lift`), and representing it to a container
    type (`lifted`).

    Decorates like an input decorator, with the exception that when a decorated
    action is calling with a value not cast to a container type, represents them
    to a container type. The result is also presented to a container type.

    Has the ability to additionally decorate an input decorator while preserving
    actions of casting to a container type.

    Partially applicable to keyword arguments, i.e. when passing only keyword
    arguments, it is equivalent to `partial(Effect, **keywords)`.
    """

    _NO_VALUE: Final[object] = object()

    lift = property(attrgetter("_lift"))
    is_lifted = property(attrgetter("_is_lifted"))

    def __new__(
        cls,
        decorator: Optional[Callable[
            Callable[V, R | C],
            Callable[C, C | M],
        ]] = None,
        /,
        annotation_of: Optional[Callable[[..., I], A]] = None,
        **kwargs,
    ) -> Union[
        Self,
        Callable[Callable[Callable[V, R | C], Callable[C, C | M]], Self],
        "_AnotatableEffect[V, R, C, I, A]",
    ]:
        if annotation_of is not None and cls is not _AnotatableEffect:
            return _AnotatableEffect(
                decorator,
                annotation_of=annotation_of,
                **kwargs,
            )
        elif decorator is None:
            return partial(Effect, annotation_of=annotation_of, **kwargs)
        else:
            return super().__new__(cls)

    def __init__(
        self,
        decorator: Callable[Callable[V, R], Callable[C, C | M]],
        /,
        *,
        lift: Callable[V | M, C],
        is_lifted: Callable[V | M | C, bool],
        annotation_of: None = None,
    ):
        self._decorator = decorator
        self._lift = lift
        self._is_lifted = is_lifted

    def __repr__(self) -> str:
        return f"Effect({code_like_repr_of(self._decorator)})"

    def __call__(
        self,
        action: Callable[V, R | C],
        value: Special[V | C] = _NO_VALUE,
    ) -> Callable[V | C, C] | C:
        lifted_action = fun(
            self.lifted |then>> self._decorator(action) |then>> self.lifted
        )

        return (
            lifted_action
            if value is Effect._NO_VALUE
            else lifted_action(value)
        )

    def lifted(self, value: V | M | C, /) -> C:
        """Method to represent an input value to a container type."""

        return value if self._is_lifted(value) else self._lift(value)

    def by(
        self,
        metadecorator: reformer_of[Callable[
            Callable[V, R | C],
            Callable[C, C | M],
        ]],
        /,
    ) -> Self:
        return type(self)(
            metadecorator(self._decorator),
            lift=self._lift,
            is_lifted=self._is_lifted,
        )


class _AnotatableEffect(Effect, Generic[V, R, C, I, A]):
    def __init__(
        self,
        decorator: Callable[Callable[V, R], Callable[C, C | M]],
        /,
        *,
        lift: Callable[V | M, C],
        is_lifted: Callable[V | M | C, bool],
        annotation_of: Optional[Callable[[..., I], A]] = None,
    ):
        super().__init__(decorator, lift=lift, is_lifted=is_lifted)
        self._annotation_of = _get if annotation_of is None else annotation_of

    def __getitem__(self, items: I | Tuple[I]) -> A:
        return self._annotation_of(*items_of(items))


as_effect: Callable[
    Effect[V, R, C] | Callable[Callable[V, R], Callable[C, C]],
    Effect[V, R, C],
]
as_effect = documenting_by(
    """
    Function representing an input decorator in `Effect` form.
    When an input decorator is already in the `Effect` form returns the form.
    """
)(
    on(not_(isinstance |by| Effect), Effect(lift=_get, is_lifted=yes))
)


context_effect: Callable[
    Callable[Callable[V, R], Callable[C, C]],
    Effect[V, R, contextual[Any, C]],
]
context_effect = documenting_by(
    """`Effect` constructor with container type as `contextual`."""
)(
    Effect(lift=contexted, is_lifted=isinstance |by| contextual)
)
