from functools import partial
from operator import add, mul, truediv

from act.contexting import contextual, contextually
from act.data_flow import break_
from act.flags import nothing, pointed, flag_about
from act.monads import *
from act.pipeline import then
from act.testing import case_of


test_maybe = case_of(
    (
        lambda: maybe(
            (lambda a: a + 2)
            |then>> bad
            |then>> (lambda _: "last node result")
        )(14),
        bad(16),
    ),
    (
        lambda: maybe((lambda a: a + 2) |then>> bad)(14),
        bad(16),
    ),
)


test_optionally = case_of(
    (
        lambda: optionally(
            (lambda a: a + 1)
            |then>> (lambda _: None)
            |then>> (lambda _: "last node result")
        )(1),
        None,
    ),
    (
        lambda: optionally(
            (lambda a: a + 3)
            |then>> (lambda b: b + 2)
            |then>> (lambda c: c + 1)
        )(10),
        16,
    ),
)


test_optionally_call_by = case_of(
    (lambda: optionally.call_by(10)(lambda n: n + 6), 16),
    (lambda: optionally.call_by(None)(lambda n: n + 6), None),
    (lambda: optionally.call_by(10)(None), None),
)


test_until_error = case_of(
    (
        lambda: until_error(lambda a: a + 3)(contextual("input context", 1)),
        contextual("input context", 4),
    ),
    (
        lambda: until_error((lambda a: a + 1) |then>> (lambda b: b + 2))(
            contextual("input context", 1)
        ),
        contextual("input context", 4),
    ),
    (
        lambda: (
            until_error(
                (lambda a: a + 2)
                |then>> (lambda b: b / 0)
                |then>> (lambda _: "last node result")
            )
            |then>> (lambda root: (
                tuple(map(lambda context: type(context.point), root.context)),
                root.value,
            ))
        )(contextual("input context", 4)),
        ((str, ZeroDivisionError), 6),
    ),
)


def test_showly():
    logs = list()

    showly(show=logs.append)(partial(add, 2) |then>> partial(mul, 2))(2)

    assert logs == [4, 8]


test_either = case_of(
    (lambda: either((.1, 1), (.2, 2))(contextual(.1, ...)), contextual(.1, 1)),
    (lambda: either(('...', -8), (nothing, 8))(...), contextual(8)),
    (lambda: either((0, 0), (1, 16))(contextual(4)), contextual(4)),
    (
        lambda: either(
            (lambda c: c > 10, lambda v: v * 10),
            (lambda c: c > 0, lambda v: v * 2),
        )(contextual(2, 4)),
        contextual(2, 8),
    ),
    (
        lambda: either(
            (lambda c: c > 10, lambda v: v * 10),
            (lambda c: c > 0, lambda v: v * 2),
        )(contextual(16, 6.4)),
        contextual(16, 64.),
    ),
    (
        lambda: either(
            (1, lambda v: v),
            (2, lambda _: "bad result"),
        )(contextually(1, print)),
        contextual(1, print),
    ),
    (
        lambda: either(
            (1, lambda _: "first bad result"),
            (2, lambda _: "second bad result"),
            (..., lambda v: v * 2),
        )(contextual(3, 32)),
        contextual(3, 64),
    ),
    (
        lambda: either(
            (1, "bad result"),
            (2, break_),
            (2, "bad result after \"break\""),
            (..., 8),
        )(contextual(2, 32)),
        contextual(2, 8),
    ),
)


def test_in_future():
    some = flag_about("some")

    context, value = in_future(partial(add, 3))(contextual(some, 5))

    assert value == 5
    assert context.points[0] is some

    flag, future_actoin = context.points[1]

    assert flag is in_future
    assert future_actoin() == 8


def test_in_future_with_noncontextual():
    context, value = in_future(partial(truediv, 64))(4)

    assert value == 4

    assert len(context.points) == 1
    assert context.point.context is in_future
    assert context.point.action() == 16


test_future = case_of(
    (lambda: future(4), contextual(4)),
    (
        lambda: future(contextual(contextually(print), None)),
        contextual(pointed(contextually(print)), None),
    ),
    (
        lambda: future(contextual(pointed(1, 2, 3), 1)),
        contextual(pointed(1, 2, 3), 1),
    ),
    (
        lambda: future(contextual(contextually(in_future, lambda: 4), ...)),
        contextual(pointed(parallel(4)), ...),
    ),
    (
        lambda: future(
            contextual(
                pointed(
                    contextually(in_future, lambda: 4),
                    contextually(in_future, lambda: 8),
                    contextually(in_future, lambda: 16),
                    "garbage",
                ),
                ...,
            )
        ),
        contextual(pointed(parallel(4), parallel(8), parallel(16)), ...),
    ),
)
