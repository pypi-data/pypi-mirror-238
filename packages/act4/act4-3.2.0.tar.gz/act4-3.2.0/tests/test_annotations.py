from operator import not_
from typing import Callable, Any, Iterable, Container, Union as typing_union

from pytest import mark, raises

from act.annotations import *
from act.errors import UnionError
from act.objects import val
from act.testing import case_of


test_action_of = case_of(
    (lambda: action_of[tuple()], Callable),
    (lambda: action_of[int], Callable[[int], Any]),
    (lambda: action_of[int, float], Callable[[int], float]),
    (lambda: action_of[int, float, str], Callable[[int], Callable[[float], str]]),
    (
        lambda: action_of[int, float, str, set],
        Callable[[int], Callable[[float], Callable[[str], set]]]
    ),
    (
        lambda: action_of[None, None, None],
        Callable[[None], Callable[[None], None]]
    ),
    (
        lambda: action_of['ann', 'ann', 'ann'],
        Callable[['ann'], Callable[['ann'], 'ann']],
    ),
)


test_noting = case_of(
    (lambda: notes_of(None), tuple()),
    (lambda: notes_of(list()), tuple()),
    (lambda: notes_of(pure(dirty(val()))), (dirty, pure)),
)


test_unia_creation_with_annotations = case_of(
    (lambda: Unia(int), int),
    (lambda: type(Unia(int, float)), Unia),
    (lambda: Unia[int], Unia(int)),
    (lambda: Unia[int, float], Unia(int, float)),
)


def test_unia_creation_without_annotations():
    with raises(UnionError):
        Unia()


@mark.parametrize(
    "value, unia, is_correct",
    (
        (list(), Unia[Iterable], True),
        (list(), Unia[Iterable, Container], True),
        (list(), Unia[Iterable, Container, int], False),
    ),
)
def test_unia(value: Any, unia: Unia, is_correct: bool):
    mode = (lambda r: r) if is_correct else not_

    assert mode(isinstance(value, unia))


test_union_creation = case_of(
    (lambda: Union(int), int),
    (lambda: Union[int], int),
)


test_union_comparison = case_of(
    (lambda: isinstance(4, Union(int, float)), True),
    (lambda: isinstance(4.2, Union(int, float)), True),
    (lambda: isinstance(4, Union[int, float]), True),
    (lambda: isinstance(4.2, Union[int, float]), True),
    (lambda: isinstance(None, Union(int, float)), False),
    (lambda: isinstance(None, Union(int, float)), False),
    (lambda: isinstance(None, Union[int, float]), False),
    (lambda: isinstance(None, Union[int, float]), False),
)


test_union_sum = case_of(
    (lambda: Union(int, Union(float, str)).__args__, (int, float, str)),
    (lambda: Union(int, float | str).__args__, (int, float, str)),
    (lambda: Union(int, typing_union[float, str]).__args__, (int, float, str)),
    (lambda: Union[int, Union(float, str)].__args__, (int, float, str)),
    (lambda: Union[int, float | str].__args__, (int, float, str)),
    (lambda: Union[int, typing_union[float, str]].__args__, (int, float, str)),
)
