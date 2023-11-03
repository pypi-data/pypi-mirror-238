from operator import truediv

from act.partiality import *
from act.testing import case_of


test_rpartial = case_of(
    (lambda: rpartial(lambda r: r, 0)(), 0),
    (lambda: rpartial(lambda a, b: a / b, 10)(1), 0.1),
    (lambda: rpartial(lambda a, b, *, c: a / b + c, 10, c=1)(1), 1.1),
    (lambda: rpartial(lambda a, b, *, c: a / b + c, 10)(1, c=1), 1.1),
    (lambda: rpartial(lambda a, b, *, c=10: a / b + c, 2)(4), 12),
    (
        lambda: rpartial(lambda a, *args, **kwargs: (a, *args, kwargs), 2, c=3)(1),
        (1, 2, dict(c=3))
    ),
)


test_mirrored_partial = case_of(
    (lambda: mirrored_partial(lambda a, b, c: a / b + c, 2, 3, 6)(), 4),
    (lambda: mirrored_partial(lambda a, b, c: a / b + c, 2, 3)(6), 4),
    (lambda: mirrored_partial(lambda a, b, *, c=0: a / b + c, 3, 6, c=2)(), 4),
    (lambda: mirrored_partial(lambda a, b, *, c=0: a / b + c, 3, 6)(c=2), 4),
    (lambda: mirrored_partial(lambda a, b, c, *, f=10: a/b + c/f, 20)(8, 4), 4),
)


test_will = case_of((
    lambda: will(lambda a, b: a / b)(1)(10), 0.1
))


test_rwill = case_of((
    lambda: rwill(lambda a, b: a / b)(10)(1), 0.1
))


test_partially = case_of(
    (lambda: partially(lambda a, b, c: a / b + c)(10, 2, 3), 8),
    (lambda: partially(lambda a, b, c: a / b + c)(10, 2)(3), 8),
    (lambda: partially(lambda a, b, c: a / b + c)(10)(2, 3), 8),
    (lambda: partially(lambda a, b, c: a / b + c)(10)(2)(3), 8),
    (lambda: partially(lambda: 16)(), 16),
    (lambda: partially(lambda *_: 16)(), 16),
    (lambda: partially(lambda *_, a=...: 16)(), 16),
    (lambda: partially(lambda *_, **__: 16)(), 16),
    (lambda: partially(lambda a, k=0: a + k)(k=4)(60), 64),
    (
        lambda: (
            partially(
                lambda *numbers, **kw_nubers: sum((*numbers, *kw_nubers.values()))
            )(1, 2, 5, a=5, b=3)
        ),
        16,
    )
)


test_flipped = case_of(
    (lambda: flipped(truediv)(10, 1), 0.1),
    (
        lambda: flipped(lambda a, b, c, *d, **e: (a / b + c, *d, e))(
            3, 2, 1, 60, 2, 80, first=1, second=2
        ),
        (100, 1, 2, 3, dict(first=1, second=2)),
    ),
)
