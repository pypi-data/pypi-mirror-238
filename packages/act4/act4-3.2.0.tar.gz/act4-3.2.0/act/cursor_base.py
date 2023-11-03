from copy import copy
from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce, wraps
from typing import (
    Iterable, Callable, Any, Mapping, Self, Tuple, Optional, Literal
)
import operator

from pyannotating import Special

from act.annotations import merger_of, R, reformer_of, Cn, Pm, V, O, P
from act.arguments import Arguments
from act.atomization import fun
from act.contexting import contextual, to_read, saving_context
from act.data_flow import by, to, io
from act.errors import ActionCursorError
from act.flags import flag_about
from act.objects import val
from act.partiality import flipped, rpartial, will, partial
from act.pipeline import ActionChain, bind_by, on, then, _generating_pipeline
from act.representations import code_like_repr_of
from act.scoping import value_in
from act.structures import tmap, tfilter
from act.synonyms import with_keyword, tuple_of


@dataclass(frozen=True)
class _OperationModel:
    sign: str
    priority: int | float


class _ActionCursorParameterUnionType(Enum):
    POSITIONAL = auto()
    KEYWORD = auto()


@dataclass(frozen=True, repr=False)
class _ActionCursorParameter:
    name: str
    priority: int | float
    union_type: Optional[_ActionCursorParameterUnionType] = None

    def __repr__(self) -> str:
        if self.union_type is _ActionCursorParameterUnionType.POSITIONAL:
            return f"*{self.name}"
        elif self.union_type is _ActionCursorParameterUnionType.KEYWORD:
            return f"**{self.name}"
        else:
            return self.name


class _ActionCursorUnpacking:
    cursor = property(operator.attrgetter("_cursor"))

    def __init__(self, cursor: "_ActionCursor", *, was_unpacked: bool = False):
        self._cursor = cursor
        self._was_unpacked = was_unpacked

    def __next__(self) -> Self:
        if self._was_unpacked:
            raise StopIteration

        self._was_unpacked = True
        return self


@val
class _ActionCursorNature:
    attrgetting = flag_about("attrgetting")
    itemgetting = flag_about("itemgetting")
    vargetting = flag_about("vargetting")

    binary_operation = flag_about("binary_operation")
    single_operation = flag_about("single_operation")
    operation = binary_operation | single_operation

    calling = flag_about("calling")
    setting = flag_about("setting")
    packing = flag_about("packing")

    argument_entering = flag_about("argument_entering")
    external = flag_about("external")
    atomic = argument_entering | external

    external_value_entering = flag_about("external_value_entering")

    set_by_initialization = flag_about("set_by_initialization")


class _ActionCursor(Mapping):
    _unpacking_key_template: str = "__ActionCursor_keyword_unpacking"
    _sign: bool = False

    def __init__(
        self,
        *,
        parameters: Iterable[_ActionCursorParameter] = tuple(),
        actions: ActionChain = ActionChain(),
        previous: Optional[Self] = None,
        nature: contextual = contextual(
            _ActionCursorNature.set_by_initialization,
        ),
        internal_repr: str = '...',
        is_generator_on_call: bool = False,
        is_call_generator_static: bool = False,
    ):
        self._parameters = tuple(sorted(
            set(parameters),
            key=operator.attrgetter("priority"),
            reverse=True,
        ))
        self._actions = actions
        self._previous = previous
        self._nature = nature
        self._internal_repr = internal_repr
        self._is_generator_on_call = is_generator_on_call
        self._is_call_generator_static = is_call_generator_static

    @property
    def _adapted_internal_repr(self) -> str:
        return self.__get_adapted_internal_repr()

    @property
    def _single_adapted_internal_repr(self) -> str:
        return self.__get_adapted_internal_repr(single=True)

    def _get_positional_union_parameter(self) -> Optional[_ActionCursorParameter]:
        positional_union_parameters = tfilter(
            lambda p: p.union_type is _ActionCursorParameterUnionType.POSITIONAL,
            self._parameters,
        )

        return (
            None
            if len(positional_union_parameters) == 0
            else positional_union_parameters[0]
        )

    def _get_keyword_union_parameter(self) -> Optional[_ActionCursorParameter]:
        keyword_union_parameters = tfilter(
            lambda p: p.union_type is _ActionCursorParameterUnionType.KEYWORD,
            self._parameters,
        )

        return (
            None
            if len(keyword_union_parameters) == 0
            else keyword_union_parameters[0]
        )

    def __repr__(self) -> str:
        return f"({self._get_raw_repr()})"

    def _get_raw_repr(self, *, is_in_fun: bool = False) -> str:
        start_sign = str() if is_in_fun else 'λ'

        return f"{start_sign}{{}}: {self._internal_repr}".format(
            ', '.join(map(str, self._parameters))
        )

    def __bool__(self) -> bool:
        return self._sign

    def __iter__(self) -> _ActionCursorUnpacking:
        return _ActionCursorUnpacking(self)

    def __len__(self) -> Literal[1]:
        return 1

    def __call__(self, *args, **kwargs) -> Any:
        keyword_union_parameter = self._get_keyword_union_parameter()

        if len(self._actions) == 0:
            if kwargs:
                raise ActionCursorError("extra keyword arguments")

            return self._with_packing_of(args, by=tuple)._with(
                internal_repr=(
                    f"({', '.join(map(self._repr_of, args))}"
                    f"{', ' if len(args) <= 1 else str()})"
                ),
            )

        elif self._is_generator_on_call:
            return self._(*args, **kwargs)

        return self._run(
            args,
            kwargs,
            keyword_union_parameter=keyword_union_parameter,
        )

    @staticmethod
    def _generation_transaction(
        method: Callable[Cn[Self, Pm], Self],
    ) -> Callable[Cn[Self, Pm], Self]:
        def transaction(cursor: Self, *args: Pm.args, **kwargs: Pm.kwargs) -> Self:
            created_cursor = method(cursor, *args, **kwargs)

            return created_cursor._with(
                previous=cursor,
                is_generator_on_call=created_cursor._is_generator_on_call,
            )

        return transaction

    @_generation_transaction
    def _(self, *args: Special[Self], **kwargs: Special[Self]) -> Self:
        return self._with_calling_by(*args, **kwargs)._with(
            internal_repr=f"{self._adapted_internal_repr}({{}})".format(
                ', '.join(map(self._repr_of, args))
                + (', ' if args and kwargs else str())
                + ', '.join(
                    (
                        self._repr_of(arg)
                        if self._is_keyword_for_unpacking(key)
                        else f"{key}={self._repr_of(arg)}"
                    )
                    for key, arg in kwargs.items()
                )
            ),
        )

    def set(self, value: Special[Self]) -> Self:
        return self._set(value)

    def ioset(self, value: Special[Self]) -> Self:
        return self._set(value, mutably=True)

    def be(self, action: Special[Self | Callable]) -> Self:
        return self._be(action)

    def iobe(self, action: Special[Self | Callable]) -> Self:
        return self._be(action, mutably=True)

    @_generation_transaction
    def _set(self, value: Special[Self], *, mutably: bool = False) -> Self:
        place, nature = self._nature

        if nature == _ActionCursorNature.attrgetting:
            setting = io(setattr)
        elif nature == _ActionCursorNature.itemgetting:
            def setting(obj_: Any, name: str, value: Any) -> Any:
                return (
                    tuple(io(operator.setitem)(list(obj_), name, value))
                    if isinstance(obj_, tuple)
                    else io(operator.setitem)(obj_, name, value)
                )
        else:
            raise ActionCursorError("setting without a place to set")

        return (
            self
            ._with_setting(value, in_=place, by=setting, mutably=mutably)
            ._with(internal_repr=("({} {} {})".format(
                self._internal_repr,
                '=' if mutably else '<-',
                self._repr_of(value),
            )))
        )

    def _be(
        self,
        action: Special[Self | Callable],
        *,
        mutably: bool = False,
    ) -> Self:
        if not callable(action):
            action = to(action)

        return partial(self._set, mutably=mutably)(partial(self._with, action)(
            internal_repr=f"{code_like_repr_of(action)}({self._internal_repr})"
        ))

    def keys(self) -> tuple[str]:
        return (f"{self._unpacking_key_template}_of_{id(self)}", )

    @_generation_transaction
    def __getitem__(self, key: Special[Self | Tuple[Special[Self]]]) -> Self:
        if self._is_keyword_for_unpacking(key):
            return self._with(
                internal_repr=f"**{self._single_adapted_internal_repr}"
            )

        keys = key if isinstance(key, tuple) else (key, )
        formatted_keys = f"[{', '.join(map(self._repr_of, keys))}]"

        if len(self._actions) == 0:
            packing_cursor = self._with_packing_of(keys, by=list)

            return packing_cursor._with(
                nature=contextual(key, _ActionCursorNature.packing),
                internal_repr=formatted_keys,
            )

        return (
            self
            ._with(
                will(operator.getitem) |then>> bind_by(
                    tuple_of
                    |then>> on(
                        len |then>> (operator.eq |by| 1),
                        operator.getitem |by| 0,
                    )
                    |then>> ...
                )
            )
            ._with_calling_by(*keys)
            ._with(
                internal_repr=f"{self._adapted_internal_repr}{formatted_keys}",
                nature=contextual(key, _ActionCursorNature.itemgetting),
            )
        )

    @_generation_transaction
    def __getattr__(self, name: str) -> Self:
        name = self._getting_name_by(name)

        if len(self._actions) == 0:
            nature_value = _ActionCursorNature.vargetting
            is_generator_on_call = True
            cursor = self._with(to(value_in(name, scope_in=2)), internal_repr=name)
        else:
            nature_value = _ActionCursorNature.attrgetting
            is_generator_on_call = self._is_generator_on_call
            cursor = self._with(
                getattr |by| name,
                internal_repr=f"{self._adapted_internal_repr}.{name}",
            )

        return cursor._with(
            nature=contextual(name, nature_value),
            is_generator_on_call=is_generator_on_call,
        )

    @classmethod
    def _operated_by(cls, parameter: _ActionCursorParameter) -> Self:
        return cls(
            parameters=[parameter],
            actions=ActionChain([
                to_read(lambda env, _: operator.getitem(env, parameter.name))
            ]),
            nature=contextual(_ActionCursorNature.argument_entering),
            internal_repr=parameter.name,
        )

    @classmethod
    def _lift(cls, value: Any, *, is_static: bool = False) -> Self:
        return cls(
            actions=ActionChain([saving_context(to(value))]),
            nature=contextual(_ActionCursorNature.external_value_entering),
            internal_repr=code_like_repr_of(value),
            is_call_generator_static=is_static,
        )

    def _run(
        self,
        args: tuple,
        kwargs: Mapping[str, Any],
        keyword_union_parameter: _ActionCursorParameter,
    ) -> Any:
        parameters = tfilter(lambda p: p.union_type is None, self._parameters)
        positional_union_parameter = self._get_positional_union_parameter()

        if len(args) > len(parameters) and positional_union_parameter is None:
            raise ActionCursorError(
                f"{len(args)} arguments instead of maximum {len(parameters)}"
            )

        elif len(args) < len(parameters):
            return lambda *second_args, **second_kwargs: self._run(
                args + second_args,
                kwargs | second_kwargs,
                keyword_union_parameter,
            )

        env = dict(zip(map(operator.attrgetter('name'), parameters), args))

        if positional_union_parameter is not None:
            env = {**env, positional_union_parameter.name: args[len(parameters):]}

        if keyword_union_parameter is not None:
            env = {**env, keyword_union_parameter.name: kwargs}

        return self._actions(contextual(env, None)).value

    def _of(
        self,
        action: Special[ActionChain, Callable],
        *,
        parameters: Optional[tuple[_ActionCursorParameter]] = None,
        previous: Optional[Self] = None,
        nature: Optional[contextual] = None,
        internal_repr: Optional[str] = None,
        is_generator_on_call: bool = False,
        is_call_generator_static: Optional[bool] = None,
    ) -> None:
        is_call_generator_static = (
            self._is_call_generator_static
            if is_call_generator_static is None
            else is_call_generator_static
        )

        return type(self)(
            parameters=on(None, self._parameters)(parameters),
            actions=(
                action
                if isinstance(action, ActionChain)
                else ActionChain([action])
            ),
            previous=self._previous if previous is None else previous,
            nature=on(None, self._nature)(nature),
            internal_repr=on(None, self._internal_repr)(internal_repr),
            is_generator_on_call=is_generator_on_call or is_call_generator_static,
            is_call_generator_static=is_call_generator_static,
        )

    def _with(
        self,
        action: Optional[Callable] = None,
        *,
        parameters: Optional[tuple[_ActionCursorParameter]] = None,
        previous: Optional[Self] = None,
        nature: Any = None,
        internal_repr: Optional[str] = None,
        is_generator_on_call: bool = False,
        is_call_generator_static: Optional[bool] = None,
    ) -> Self:
        return self._of(
            self._actions |then>> (
                ActionChain() if action is None else saving_context(action)
            ),
            parameters=parameters,
            previous=previous,
            nature=nature,
            internal_repr=internal_repr,
            is_generator_on_call=is_generator_on_call,
            is_call_generator_static=is_call_generator_static,
        )

    @_generation_transaction
    def _merged_with(self, other: Special[Self], *, by: merger_of[Any]) -> Self:
        operation = by

        if (
            isinstance(other, _ActionCursor)
            and self._is_call_generator_static is not other._is_call_generator_static
        ):
            raise ActionCursorError("combining dynamic and static cursors")

        cursor = (
            self._of(
                ActionChain([lambda root: contextual(
                    root.context,
                    operation(self._actions(root).value, other._actions(root).value),
                )]),
                parameters=self._parameters + other._parameters,
                is_call_generator_static=(
                    self._is_call_generator_static
                    or other._is_call_generator_static
                ),
            )
            if isinstance(other, _ActionCursor)
            else self._with(rpartial(operation, other))
        )

        return cursor._with(nature=contextual(
            contextual(other, operation),
            _ActionCursorNature.binary_operation,
        ))

    @_generation_transaction
    def _with_calling_by(
        self,
        *args: Special[Self],
        **kwargs: Special[Self],
    ) -> Self:
        return (
            self
            ._with_partial_application_from(args)
            ._with_keyword_partial_application_by(kwargs)
            ._with(operator.call, nature=contextual(
                Arguments(args, kwargs),
                _ActionCursorNature.calling,
            ))
        )

    @_generation_transaction
    def _with_partial_application_from(
        self,
        arguments: Iterable[Special[Self]],
    ) -> Self:
        arguments = tuple(arguments)

        if not arguments:
            return self

        return reduce(
            lambda cursor, argument: (
                cursor._merged_with(
                    argument.cursor,
                    by=lambda a, b: partial(a, *b)
                )
                if isinstance(argument, _ActionCursorUnpacking)
                else cursor._merged_with(argument, by=partial)
            ),
            (self, *arguments),
        )

    @_generation_transaction
    def _with_keyword_partial_application_by(
        self,
        argument_by_key: Mapping[str, Special[Self]],
    ) -> Self:
        if not argument_by_key.keys():
            return self

        return reduce(
            lambda cursor, key_and_argument: (cursor._merged_with(
                key_and_argument[1],
                by=(
                    lambda a, b: partial(a, **b)
                    if self._is_keyword_for_unpacking(key_and_argument[0])
                    else flipped(with_keyword |to| key_and_argument[0])
                ),
            )),
            (self, *argument_by_key.items()),
        )

    @_generation_transaction
    def _with_setting(
        self,
        value: V | Self,
        *,
        in_: P,
        by: Callable[[O, P, V], R],
        mutably: bool = False
    ) -> Self:
        place = in_
        set_ = by

        return (
            self._previous
            ._merged_with(value, by=lambda a, b: lambda p: (
                set_(a if mutably else copy(a), p, b)
            ))
            ._with_calling_by(place)
            ._with(nature=contextual(
                contextual(place, value),
                _ActionCursorNature.setting,
            ))
        )

    @_generation_transaction
    def _with_packing_of(
        self,
        items: Iterable[Special[Self]],
        *,
        by: Callable[[tuple], Iterable],
    ) -> Self:
        items = tuple(items)

        return (
            self
            ._with(to(tuple_of))
            ._with_calling_by(*items)
            ._with(by, nature=contextual(
                contextual(tuple(items), by),
                _ActionCursorNature.packing,
            ))
        )

    def _is_keyword_for_unpacking(self, keyword: Special[str]) -> bool:
        return (
            isinstance(keyword, str)
            and keyword.startswith(self._unpacking_key_template)
        )

    def _getting_name_by(self, name: str) -> str:
        for attribute_name in dir(self):
            if (
                name.startswith(attribute_name)
                and all(map(operator.eq |by| '_', name[len(attribute_name) + 1:]))
            ):
                return name[:-1]

        return name

    def __fun_image__(self) -> fun.Image:
        keyword_union_parameter = self._get_keyword_union_parameter()

        def run(*args, **kwargs) -> Any:
            return self._run(
                args,
                kwargs,
                keyword_union_parameter=keyword_union_parameter,
            )

        return fun.Image(run, partial(self._get_raw_repr, is_in_fun=True))

    def _internal_repr_by(
        self,
        model: _OperationModel,
        *,
        on_left_side: bool = True,
    ) -> str:
        return (
            f"({self._internal_repr})"
            if (
                self._nature.value == _ActionCursorNature.operation
                and isinstance(self._nature.context, _OperationModel)
                and (operator.gt if on_left_side else operator.ge)(
                    self._nature.context.priority,
                    model.priority,
                )
            )
            else self._internal_repr
        )

    @staticmethod
    def _repr_of(value: Special[Self]) -> str:
        if isinstance(value, _ActionCursor):
            return value._internal_repr

        elif isinstance(value, _ActionCursorUnpacking):
            return f"*{value.cursor._single_adapted_internal_repr}"

        else:
            return code_like_repr_of(value)

    def __get_adapted_internal_repr(self, *, single: bool = False) -> str:
        return (
            f"({self._internal_repr})"
            if (
                self._internal_repr == '...'
                or (
                    not single
                    and self._nature.value == _ActionCursorNature.operation
                )
            )
            else self._internal_repr
        )

    @staticmethod
    def __merging_by(
        operation: merger_of[Any],
        model: _OperationModel,
        *,
        is_right: bool = False,
    ) -> Callable[[Self, Special[Self]], Self]:
        def cursor_merger(cursor: Self, value: Special[Self]) -> Self:
            if len(cursor._actions) == 0:
                raise ActionCursorError("interaction with external cursor")

            internal_repr = cursor._internal_repr_by(
                model,
                on_left_side=not is_right
            )

            return (
                cursor
                ._merged_with(
                    value,
                    by=flipped(operation) if is_right else operation,
                )
                ._with(
                    nature=contextual(model, _ActionCursorNature.binary_operation),
                    internal_repr=(
                        (
                            f"{internal_repr} {model.sign} {{}}"
                            if not is_right
                            else f"{{}} {model.sign} {internal_repr}"
                        ).format(
                            value._internal_repr_by(model, on_left_side=is_right)
                            if isinstance(value, _ActionCursor)
                            else _ActionCursor._repr_of(value)
                        )
                    )
                )
            )

        return cursor_merger

    @staticmethod
    def __transformation_by(
        operation: Callable[[Special[Self]], R],
        model: _OperationModel,
    ) -> reformer_of[Self]:
        def cursor_transformer(cursor: Self) -> Self:
            return cursor._with(
                operation,
                nature=contextual(model, _ActionCursorNature.single_operation),
                internal_repr=f"{model.sign}{cursor._internal_repr_by(model)}",
            )

        return cursor_transformer

    @staticmethod
    def __with_forced_sign(forced_sign: bool) -> reformer_of[Callable[Pm, Self]]:
        def decorator(action: Callable[Pm, Self]) -> Callable[Pm, Self]:
            @wraps(action)
            def action_with_forced_sign(*args: Pm.args, **kwargs: Pm.kwargs) -> Self:
                cursor = action(*args, **kwargs)
                cursor._sign = forced_sign

                return cursor

            return action_with_forced_sign

        return decorator

    is_ = __merging_by(operator.is_, _OperationModel('is', 8))
    is_not = __merging_by(operator.is_not, _OperationModel("is not", 8))
    in_ = __merging_by(flipped(operator.contains), _OperationModel('in', 8))
    not_in = __merging_by(
        flipped(operator.contains) |then>> operator.not_,
        _OperationModel('not in', 8),
    )
    has = __merging_by(operator.contains, _OperationModel("contains", 8))
    has_no = __merging_by(
        operator.contains |then>> operator.not_,
        _OperationModel("contains no", 8),
    )
    and_ = __merging_by(lambda a, b: a and b, _OperationModel('and', 9))
    or_ = __merging_by(lambda a, b: a or b, _OperationModel('or', 10))

    __pos__ = __transformation_by(operator.pos, _OperationModel('+', 1))
    __neg__ = __transformation_by(operator.neg, _OperationModel('-', 1))
    __invert__ = __transformation_by(operator.invert, _OperationModel('~', 1))

    __pow__ = __merging_by(operator.pow, _OperationModel('**', 0))
    __mul__ = __merging_by(operator.mul, _OperationModel('*', 2))
    __floordiv__ = __merging_by(operator.floordiv, _OperationModel('//', 2))
    __truediv__ = __merging_by(operator.truediv, _OperationModel('/', 2))
    __matmul__ = __merging_by(operator.matmul, _OperationModel('@', 2))
    __mod__ = __merging_by(operator.mod, _OperationModel('%', 2))
    __add__ = __merging_by(operator.add, _OperationModel('+', 3))
    __sub__ = __merging_by(operator.sub, _OperationModel('-', 3))
    __lshift__ = __merging_by(operator.lshift, _OperationModel('<<', 4))
    __rshift__ = __merging_by(operator.rshift, _OperationModel('>>', 4))
    __and__ = __merging_by(operator.and_, _OperationModel('&', 5))
    __xor__ = __merging_by(operator.xor, _OperationModel('^', 6))
    __or__ = _generating_pipeline(__merging_by(
        operator.or_,
        _OperationModel('|', 7),
    ))

    __rpow__ = __merging_by(operator.pow, _OperationModel('**', 0), is_right=True)
    __rmul__ = __merging_by(operator.mul, _OperationModel('*', 2), is_right=True)
    __rfloordiv__ = __merging_by(
        operator.floordiv,
        _OperationModel('//', 2), is_right=True,
    )
    __rtruediv__ = __merging_by(
        operator.truediv,
        _OperationModel('/', 2), is_right=True,
    )
    __rmatmul__ = __merging_by(
        operator.matmul,
        _OperationModel('@', 2), is_right=True,
    )
    __rmod__ = __merging_by(operator.mod, _OperationModel('%', 2), is_right=True)
    __radd__ = __merging_by(operator.add, _OperationModel('+', 3), is_right=True)
    __rsub__ = __merging_by(operator.sub, _OperationModel('-', 3), is_right=True)
    __rlshift__ = __merging_by(
        operator.lshift,
        _OperationModel('<<', 4), is_right=True,
    )
    __rrshift__ = __merging_by(
        operator.rshift,
        _OperationModel('>>', 4), is_right=True,
    )
    __rand__ = __merging_by(operator.and_, _OperationModel('&', 5), is_right=True)
    __rxor__ = __merging_by(operator.xor, _OperationModel('^', 6), is_right=True)
    __ror__ = __merging_by(operator.or_, _OperationModel('|', 7), is_right=True)

    __gt__ = __with_forced_sign(False)(
        __merging_by(operator.gt, _OperationModel('>', 8))
    )
    __lt__ = __with_forced_sign(False)(
        __merging_by(operator.lt, _OperationModel('<', 8))
    )
    __ge__ = __with_forced_sign(False)(
        __merging_by(operator.ge, _OperationModel('>=', 8))
    )
    __le__ = __with_forced_sign(False)(
        __merging_by(operator.le, _OperationModel('>=', 8))
    )
    __ne__ = __with_forced_sign(True)(
        __merging_by(operator.ne, _OperationModel('!=', 8))
    )
    __eq__ = __with_forced_sign(False)(
        __merging_by(operator.eq, _OperationModel('==', 8))
    )


def _dynamic(cursor: _ActionCursor) -> Self:
    return cursor._with(is_call_generator_static=False)


def _static(cursor: _ActionCursor) -> Self:
    return cursor._with(is_call_generator_static=True)


def _normilized(numbers: Iterable[int]) -> list[int]:
    normilized_numbers = list()

    for current_number in numbers:
        smaller_number_counter = 0

        for target_number in numbers:
            if current_number > target_number:
                smaller_number_counter += 1

        normilized_numbers.append(smaller_number_counter)

    return normilized_numbers


def _fn(*cursors: _ActionCursor) -> Callable[_ActionCursor, Callable]:
    if len(cursors) == 0:
        return fun

    parameter_cursors = list()
    void_parameter_indexes = list()

    for index, cursor in enumerate(parameter_cursors):
        if cursor in [_, act]:  # noqa: F821
            void_parameter_indexes.append(index)
        else:
            parameter_cursors.append(cursor)

    if len(frozenset(map(id, parameter_cursors))) != len(parameter_cursors):
        return ActionCursorError("repeating parameters")

    has_kwargs = kwargs is parameter_cursors[-1]  # noqa: F821
    has_args: bool

    if has_kwargs:
        has_args = (
            False
            if len(parameter_cursors) == 1
            else args is parameter_cursors[-2]  # noqa: F821
        )
    else:
        has_args = args is parameter_cursors[-1]  # noqa: F821

    required_parameters_length = (
        len(parameter_cursors) - int(has_args) - int(has_kwargs)
    )
    required_parameter_cursors = parameter_cursors[:required_parameters_length]

    for cursor in required_parameter_cursors:
        if cursor._natrue.value != _ActionCursorNature.atomic:
            raise ActionCursorError("calculation parameters")
        if cursor is args:  # noqa: F821
            raise ActionCursorError("parameters after `args`")
        if cursor is kwargs:  # noqa: F821
            raise ActionCursorError("`kwargs` not at the end of parameters")

    required_parameters = tmap(
        lambda c: c._parameters[0],
        required_parameter_cursors,
    )

    argument_order = _normilized(  # noqa: F841
        tmap(lambda p: p.priority, required_parameters)
    )

    def decorator(main: _ActionCursor) -> Callable:
        if _is_parameters_non_matching(required_parameters, main._parameters):
            raise ActionCursorError("non-matching parameters to arguments")

        def func(*args, **kwargs):
            if not has_kwargs and kwargs:
                raise ActionCursorError("keyword arguments")


def _is_parameters_non_matching(
    first_parameters: tuple[_ActionCursorParameter],
    second_parameters: tuple[_ActionCursorParameter],
) -> bool:
    return (
        len(first_parameters) == len(second_parameters)
        and frozenset(first_parameters) == frozenset(second_parameters)
    )
