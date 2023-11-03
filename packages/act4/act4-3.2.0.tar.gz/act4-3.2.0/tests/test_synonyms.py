from typing import Callable, Iterable, Type

from act.synonyms import *
from act.testing import case_of
from tests.mocks import CustomContext, fail_by_error, Counter

from pytest import mark, raises


test_raise_ = case_of(
    (lambda: with_(raises(TypeError), lambda _: raise_(TypeError())), None),
)


test_assert_ = case_of(
    (lambda: assert_(16), None),
    (lambda: with_(raises(AssertionError), lambda _: assert_(None)), None),
)


test_on = case_of(
    (lambda: on(lambda x: x > 0, lambda x: x ** x)(4), 256),
    (lambda: on(lambda x: x > 0, lambda x: x ** x)(-4), -4),
    (lambda: on(lambda x: x > 0, lambda x: x ** x)(-4), -4),
    (lambda: on(lambda x: x > 0, lambda _: _, else_=lambda x: -x)(4), 4),
    (lambda: on(lambda x: x > 0, lambda _: _, else_=lambda x: -x)(-4), 4),
    (lambda: on(False, True)(False), True),
    (lambda: on(False, True)(None), None),
    (lambda: on(False, True, else_=None)(True), None),
)


test_while_ = case_of(
    (lambda: while_(lambda x: x < 10, lambda x: x + 1)(0), 10),
    (lambda: while_(lambda x: x > 0, lambda x: x - 1)(0), 0),
)


@mark.parametrize(
    "number_of_handler_calls, number_of_checker_calls",
    [(i, i + 1) for i in range(3)] + [(100, 101), (653, 654), (999, 1000)]
)
def test_while__execution_sequences(
    number_of_handler_calls: int,
    number_of_checker_calls: int
):
    handling_counter = Counter()
    checking_counter = Counter()

    while_(
        lambda _: (
            checking_counter()
            or checking_counter.counted < number_of_checker_calls
        ),
        lambda _: handling_counter(),
    )(None)

    assert number_of_handler_calls == handling_counter.counted
    assert number_of_checker_calls == checking_counter.counted


test_try__without_error = case_of(
    (lambda: try_(lambda a: 1 / a, lambda _: fail_by_error)(10), 0.1),
    (lambda: try_(lambda a, b: a + b, lambda _: fail_by_error)(5, 3), 8),
    (lambda: try_(lambda a, b: a + b, lambda _: fail_by_error)(5, b=3), 8),
    (lambda: try_(lambda: 256, lambda _: fail_by_error)(), 256),
)


@mark.parametrize(
    "func, input_args, error_type",
    [
        (lambda x: x / 0, (42, ), ZeroDivisionError),
        (lambda x, y: x + y, (1, '2'), TypeError),
        (lambda mapping, key: mapping[key], (tuple(), 0), IndexError),
        (lambda mapping, key: mapping[key], (tuple(), 10), IndexError),
        (lambda mapping, key: mapping[key], ((1, 2), 2), IndexError),
        (lambda mapping, key: mapping[key], (dict(), 'a'), KeyError),
        (lambda mapping, key: mapping[key], ({'a': 42}, 'b'), KeyError),
        (lambda: int('1' + '0'*4300), tuple(), ValueError)
    ]
)
def test_try__with_error(
    func: Callable,
    input_args: Iterable,
    error_type: Type[Exception]
):
    assert (
        type(try_(func, lambda *_: lambda error: error)(*input_args))
        is error_type
    )


test_with_ = case_of(
    (lambda: with_(CustomContext(256), lambda v: v), 256),
    (lambda: with_(CustomContext(16))(lambda v: v), 16),
)


test_keyword_unpackly = case_of((
    lambda: keyword_unpackly(lambda a, b, c: (c, b, a))(dict(a=1, b=2, c=3)),
    (3, 2, 1),
))


test_tuple_of = case_of(
    (lambda: tuple_of(1, 2, 3), (1, 2, 3)),
    (lambda: tuple_of(), tuple()),
)


test_in_tuple = case_of((
    lambda: in_tuple(8), (8, )
))


test_with_keyword = case_of((
    with_keyword('a', 3, lambda a, b=5: a + b), 8
))
