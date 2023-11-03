from collections import OrderedDict
from math import copysign
from operator import methodcaller, contains
from types import MappingProxyType
from typing import (
    Iterable, Tuple, Callable, Mapping, TypeAlias, Optional, Self, Iterator,
    Generator
)

from pyannotating import many_or_one, Special

from act.annotations import V, M, K, I, W, Unia
from act.atomization import fun
from act.contexting import ContextualForm, contexted, contextualizing, saving_context
from act.data_flow import io, by, and_via_indexer, indexer_of
from act.errors import RangeConstructionError, IndexingError
from act.flags import flag_about
from act.objects import val
from act.partiality import partial, rpartial, partially, will, rwill
from act.pipeline import then, bind_by, ActionChain
from act.protocols import Hashable
from act.representations import code_like_repr_of
from act.synonyms import on, tuple_of, while_
from act.tools import documenting_by


__all__ = (
    "frozendict",
    "as_collection",
    "tmap",
    "tzip",
    "tfilter",
    "flat",
    "deep_flat",
    "append",
    "without",
    "without_duplicates",
    "slice_from",
    "interval",
    "Interval",
    "ranges_from",
    "range_from",
    "filled",
    "empty",
    "marked_ranges_from",
    "to_interval",
    "groups_in",
    "indexed",
    "table",
)


frozendict: TypeAlias = MappingProxyType


as_collection: Callable[[many_or_one[V]], Tuple[V]]
as_collection = documenting_by(
    """
    Function to convert an input value into a tuple collection.
    With a non-iterable value, wraps it in a tuple.
    """
)(
    on(rpartial(isinstance, Iterable), tuple, else_=tuple_of)
)


tmap: Callable[Iterable[V], Tuple[V]]
tmap = documenting_by("""`map` function returning `tuple`""")(
    fun(map |then>> tuple)
)


tzip: Callable[Iterable[V], Tuple[V]]
tzip = documenting_by("""`zip` function returning `tuple`""")(
    fun(zip |then>> tuple)
)


tfilter: Callable[Iterable[V], Tuple[V]]
tfilter = documenting_by("""`filter` function returning `tuple`""")(
    fun(filter |then>> tuple)
)


def flat(value: V | Iterable[Special[Iterable, V]]) -> Tuple[V]:
    """Function to expand input collection's subcollections to it."""

    collection_with_opened_items = list()

    for item in as_collection(value):
        if not isinstance(item, Iterable):
            collection_with_opened_items.append(item)
            continue

        collection_with_opened_items.extend(item)

    return tuple(collection_with_opened_items)


deep_flat: Callable[V | Special[Iterable, V], Tuple[V]]
deep_flat = documenting_by(
    """
    Function to expand all subcollections within an input collection while they
    exist.
    """
)(fun(
    as_collection
    |then>> while_(partial(tfilter, rpartial(isinstance, Iterable)), flat)
))


append: Callable[..., Callable[Iterable[V] | V, tuple]]
append = documenting_by(
    """
    Function for a function that adds input arguments of the first function to
    an input collection of the returned function, or forms a collection with
    all of these elements in case a non-collection was passed to the returned
    function.
    """
)(fun(
    tuple_of
    |then>> rwill(tuple_of)
    |then>> bind_by(as_collection |then>> ... |then>> flat)
    |then>> fun
))


def without(*items: I) -> Callable[I | Iterable[I], Tuple[I]]:
    """
    Function for an action that represents an input value as a `tuple` with no
    items passed to this function.
    """

    removing = ActionChain(
        io(on(contains |by| item, methodcaller("remove", item)))
        for item in items
    )

    return fun(as_collection |then>> list |then>> removing |then>> tuple)


def without_duplicates(items: Iterable[V]) -> Tuple[V]:
    """Function to get collection without duplicates."""

    items_without_duplicates = list()

    for item in items:
        if item not in items_without_duplicates:
            items_without_duplicates.append(item)

    return tuple(items_without_duplicates)


def slice_from(range_: range) -> slice:
    """Function to cast an input `range` to a `slice`."""

    return slice(range_.start, range_.stop, range_.step)


class _SliceGenerator:
    def __init__(self, name: str, *, slices: Iterable[slice] = tuple()):
        self._name = name
        self._sleces = tuple(slices)

    def __repr__(self) -> str:
        return (
            self._name
            + str().join(map(self.__native_slice_repr_of, self._sleces))
        )

    def __getitem__(self, key: int | slice) -> Self:
        return type(self)(
            self._name,
            slices=(
                *self._sleces,
                key if isinstance(key, slice) else self.__slice_of(key),
            )
        )

    def __iter__(self) -> Iterator[slice]:
        return iter(self._sleces)

    @staticmethod
    def __slice_of(number: int) -> slice:
        return (
            slice(number, number + 1)
            if number >= 0
            else slice(number, number - 1, -1)
        )

    @staticmethod
    def __native_slice_repr_of(slice_: slice) -> str:
        return "[{}:{}:{}]".format(*map(
            on(None, str()),
            (slice_.start, slice_.stop, slice_.step),
        ))


interval = documenting_by(
    """
    Object to generate `slices` via indexer (`[]`).
    Iterable over generated `slices`.
    """
)(
    _SliceGenerator("interval")
)


IntervalSegment: TypeAlias = int | range | slice
Interval: TypeAlias = IntervalSegment | Iterable[IntervalSegment]


def ranges_from(interval: Interval, *, limit: Optional[int] = None) -> Tuple[range]:
    """
    Function to get `ranges` from unstructured value or a collection of them.
    """

    intervals = (
        (interval, )
        if isinstance(interval, IntervalSegment)
        else tuple(interval)
    )

    return tmap(partial(range_from, limit=limit), intervals)


def range_from(
    interval_segment: IntervalSegment,
    *,
    limit: Optional[int] = None,
) -> range:
    """Function to get `ranges` from unstructured value"""

    if isinstance(interval_segment, slice):
        return _range_from_slice(interval_segment, limit=limit)
    elif isinstance(interval_segment, range):
        range_ = interval_segment
    else:
        range_ = range(interval_segment, interval_segment + 1)

    return range_


def _range_from_slice(slice_: slice, *, limit: Optional[int]) -> range:
    start = 0 if slice_.start is None else slice_.start
    stop = 0 if slice_.stop is None else slice_.stop
    step = 1 if slice_.step is None else slice_.step

    if slice_.start is None and copysign(1, stop) != copysign(1, step):
        raise RangeConstructionError("unable to determine start of range")

    if slice_.stop is None:
        if limit is None or start >= limit and step > 0:
            return range(0, 0)

        stop = limit if step > 0 else -1

    if slice_.step is None:
        step = int(copysign(1, stop - start))

    return range(start, stop, step)


filled = contextualizing(flag_about("filled"))
empty = contextualizing(flag_about("empty"))


def marked_ranges_from(
    points: Iterable[int],
) -> Tuple[filled[range] | empty[range]]:
    """
    Function to create `ranges` from input numbers and `ranges` between them.
    """

    points = sorted(set(points))

    marked_ranges = list()
    last_range_start = points[0]

    for current, next_ in indexed(points, 0, 1):
        if current + 1 == next_:
            continue

        marked_ranges.append(filled(range(last_range_start, current + 1)))
        marked_ranges.append(empty(range(current + 1, next_)))
        last_range_start = next_

    marked_ranges.append(filled(range(last_range_start, points[-1] + 1)))

    return tuple(marked_ranges)


class _curried_to_interval:
    def __init__(self, interval: Iterable[slice | int] = tuple()):
        self._interval = tuple(interval)

    def __repr__(self) -> str:
        return "to_interval{}".format(str().join(
            f"[{code_like_repr_of(segment)}]"
            for segment in self._interval
        ))

    def __call__(
        self,
        action: Callable[Tuple[V], Iterable[V]],
        values: Optional[Iterable[V]] = None,
    ) -> Tuple[V] | Callable[Iterable[W], Tuple[W]]:
        return (
            to_interval(self._interval, action, values)
            if values is not None
            else partial(self, action)
        )

    def __getitem__(self, segment: slice | int) -> Self:
        return type(self)((*self._interval, segment))


@and_via_indexer(indexer_of(_curried_to_interval()))
@partially
def to_interval(
    interval: Interval | ContextualForm[empty | filled, Interval],
    action: Callable[Tuple[V], Iterable[V]],
    values: Iterable[V],
) -> Tuple[V]:
    """
    Function to apply an action from collection to a part of an input collection.

    Specifies a part of an input collection that will be affected by an
    unstructured range.
    """

    values = tuple(values)

    if contexted(interval).context == empty:
        return values

    points = (
        will(map)(lambda p: len(values) + p if p < 0 else p)
        |then>> will(tfilter)(lambda p: p < len(values))
    )(flat(ranges_from(contexted(interval).value, limit=len(values))))

    if len(points) == 0:
        return values

    if set(points) == set(range(len(values))):
        return tuple(action(values))

    marked_ranges = marked_ranges_from(points)

    if min(points) > 0:
        marked_ranges = (empty(range(0, min(points))), *marked_ranges)

    if max(points) != len(values) - 1:
        marked_ranges = (*marked_ranges, empty(range(max(points) + 1, len(values))))

    return flat(
        to_interval(
            saving_context(len |then>> range)(marked_range),
            action,
            values[slice_from(marked_range.value)],
        )
        for marked_range in marked_ranges
    )


def groups_in(
    items: Iterable[V],
    by: Callable[V, Unia[I, Hashable]],
) -> OrderedDict[Unia[I, Hashable], V]:
    """
    Function of selecting groups among the elements of an input collection.
    Segregates elements by id resulting from calling the `by` argument.
    """

    id_by_item = table.from_keys(items, by)
    group_by_id = OrderedDict.fromkeys(id_by_item.values(), tuple())

    for item in items:
        group_by_id[id_by_item[item]] = (*group_by_id[id_by_item[item]], item)

    return group_by_id


def indexed(items: Iterable[V], *indexes: int) -> Generator[Tuple[V], None, None]:
    """Function to get ordered items under input indexes."""

    items = tuple(items)

    if any(index < 0 for index in indexes):
        raise IndexingError("indexes must be positive")

    if len(items) - max(indexes) < 0:
        raise IndexingError(
            f"there must be {max(indexes)} or more items to index",
        )

    index_border = len(items) - max(indexes)

    for current_index in range(index_border):
        yield tuple(items[current_index + index] for index in indexes)


@val
class table:
    def map(mapped: Callable[V, M], table: Mapping[K, V]) -> OrderedDict[K, M]:
        """
        Function to map values of an input `Mapping` object by an input action.

        Saves sequence.
        """

        return OrderedDict((_, mapped(value)) for _, value in table.items())

    def filter(
        is_valid: Callable[V, bool],
        table: Mapping[K, V],
    ) -> OrderedDict[K, V]:
        """
        Function to filter values of an input `Mapping` object by an input
        action.

        Saves sequence.
        """

        return OrderedDict(
            (_, value) for _, value in table.items() if is_valid(value)
        )

    def from_keys(
        keys: Iterable[K],
        value_of: Callable[[K], V] = lambda _: None,
    ) -> OrderedDict[K, V]:
        """
        Function to create a `Mapping` with keys from an input collection and
        values obtained by applying an input action to a key under which a
        resulting value will be stored.

        Saves sequence.
        """

        return OrderedDict((key, value_of(key)) for key in keys)

    def reversed(table: Mapping[K, V]) -> OrderedDict[V, K]:
        """
        Function to swap keys and values in `Mapping`.

        Saves sequence.
        """

        return OrderedDict(map(reversed, table.items()))
