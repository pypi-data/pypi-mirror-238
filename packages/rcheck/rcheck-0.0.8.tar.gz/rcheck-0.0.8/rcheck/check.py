from __future__ import annotations

from collections.abc import (
    Callable,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Sequence,
    Set,
)
from typing import (
    Any,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
    overload,
)

# references:
# * https://github.com/dagster-io/dagster/blob/498e3f1da1fa3ed6c548bff26e74c6c3e05fd140/python_modules/dagster/dagster/_check/__init__.py
# * https://github.com/pydantic/pydantic/blob/6ed90daab74767ce94ee4d2413f02f42b73a53f6/pydantic/v1/validators.py


T = TypeVar("T")
KT = TypeVar("KT")
VT = TypeVar("VT")


class BaseException(Exception):
    type_: Type[Any]
    
    def __init__(
        self,
        name: str,
        value: Any,
        description: Optional[str] = None,
    ):
        self._name = name
        self._value = value
        self._description = description

    def __str__(self):
        output = f"Error in param: {self._name} got value {self._value} is not of type {self.type_.__name__}."

        if self._description is not None:
            output += "\n\n" + self._description

        return output


class StrException(BaseException):
    type_ = str


class BytesException(BaseException):
    type_ = bytes


class BoolException(BaseException):
    type_ = bool


class FloatException(BaseException):
    type_ = float


class IntException(BaseException):
    type_ = int


class SequenceException(BaseException):
    type_ = Sequence


class MutableSequenceException(BaseException):
    type_ = MutableSequence


class SetException(BaseException):
    type_ = Set


class MutableSetException(BaseException):
    type_ = MutableSet


class MappingException(BaseException):
    type_ = Mapping


class MutableMappingException(BaseException):
    type_ = MutableMapping


class SequenceOfException(BaseException):
    type_ = Sequence


class SetOfException(BaseException):
    type_ = Set


class MutableSequenceOfException(BaseException):
    type_ = MutableSequence


class MutableSetOfException(BaseException):
    type_ = MutableSet


def is_optional(type_: Type[Any]):
    return type(None) in get_args(type_)


def remove_optional(type_: Type[Any]):
    if not is_optional(type_):
        return type_

    args = get_args(type_)

    if len(args) == 2:
        none_index = args.index(type(None))
        return args[1 - none_index]

    # deep copy
    return_type = Union[int, None]  # could be anything
    return_type.__dict__ = type_.__dict__.copy()

    setattr(return_type, "__args__", tuple(arg for arg in args if arg != type(None)))

    return return_type


class CheckAll:
    def __init__(self, *, check_instance: Check):
        self.check = check_instance

    def __enter__(self):
        return self.check

    def __exit__(self, exc_type, exc_value, exc_tb):
        # non rcheck errors
        if exc_type is not None:
            return True

        records = self.check._records

        if len(records) == 0:
            if self.check._suppress_and_record_original:
                r._disable_suppress_and_record()

            return False

        if len(records) == 1:
            raise records[0]

        raise ExceptionGroup("Multiple rcheck validation errors occured", records)


def check_all():
    """
    Usage (need to replace all `r.check_*` with `checker.check_*` or whatever variable name you decide):
    ```
    with check_all() as checker:
        checker.check_str("str name", possible_str)
    ```
    """
    return CheckAll(check_instance=Check(suppress_and_record=True))


def _convert_tuple_to_union(type_: Type[Any]) -> Type[Any]:
    if isinstance(type_, tuple):
        tmp_type_ = Union[int, float]  # could be anything
        setattr(tmp_type_, "__args__", type_)
        type_ = tmp_type_

    return type_


class Check:
    def __init__(self, *, suppress_and_record: bool = False):
        self._suppress_and_record = suppress_and_record
        self._suppress_and_record_original = suppress_and_record

        if suppress_and_record:
            self._enable_suppress_and_record()

    def _enable_suppress_and_record(self):
        self._suppress_and_record = True
        self._records: List[BaseException] = []

    def _disable_suppress_and_record(self):
        del self._records
        self._suppress_and_record = False

    def _error(self, exception: Exception):
        if self._suppress_and_record:
            self._records.append(exception)
            return

        raise exception

    def _generic_isinstance(self, value: Any, type_: Type[Any]) -> Tuple[bool, Any]:
        # print("generic isinstaance", value, type_)
        # print(value, type_)
        type_ = _convert_tuple_to_union(type_)

        if type_ == Any:
            return True, {}

        is_opt = is_optional(type_)
        type_ = remove_optional(type_)

        origin = get_origin(type_)
        args = get_args(type_)

        # or could call the check_opt_* version of checks?
        if is_opt and value is None:
            return True, {}

        checker = Check(suppress_and_record=False)

        if origin == Union:
            # print("IN UNION", args)
            for union_type in args:
                is_type, desc = self._generic_isinstance(value, union_type)
                if is_type:
                    return True, {}

            return False, {}
        elif origin == MutableSequence:
            try:
                checker.check_mutable_sequence("fake-seq-name", value, of=args[0])
                return True, {}
            except BaseException:
                return False, {}
        elif origin == Sequence:
            # print("seq", args)
            try:
                checker.check_sequence("fake-seq-name", value, of=args[0])
                return True, {}
            except BaseException:
                # print("ret false")
                return False, {}
        elif origin == MutableMapping:
            k_args, v_args = args
            try:
                checker.check_mutable_mapping(
                    "fake-seq-name", value, keys_of=k_args, values_of=v_args
                )
                return True, {}
            except BaseException:
                return False, {}
        elif origin == Mapping:
            k_args, v_args = args
            # print("mapping", k_args, v_args)
            try:
                checker.check_mapping(
                    "fake-seq-name", value, keys_of=k_args, values_of=v_args
                )
                return True, {}
            except BaseException:
                return False, {}
        elif origin == MutableSet:
            try:
                checker.check_mutable_set("fake-seq-name", value, of=args[0])
                return True, {}
            except BaseException:
                return False, {}
        elif origin == Set:
            try:
                checker.check_set("fake-seq-name", value, of=args[0])
                return True, {}
            except BaseException:
                return False, {}
        elif isinstance(value, type_):
            return True, {}

        return False, {}

    def check_str(
        self,
        name: str,
        value: Any,
        *,
        description: Optional[str] = None,
    ) -> str:
        if isinstance(value, str):
            return value

        self._error(StrException(name, value, description))
        return "rcheck placeholder for check_all contextes. this check resulted in an error and was used before the end of the check_all context. refrain from doing this."

    @overload
    def check_opt_str(
        self,
        name: str,
        value: Any,
        *,
        description: Optional[str] = None,
    ) -> Optional[str]:
        ...

    @overload
    def check_opt_str(
        self,
        name: str,
        value: Any,
        *,
        default: str,
        description: Optional[str] = None,
    ) -> str:
        ...

    def check_opt_str(
        self,
        name: str,
        value: Any,
        *,
        default: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[str]:
        if value is None:
            return default

        return self.check_str(name, value, description=description)

    def check_bytes(
        self,
        name: str,
        value: Any,
        *,
        description: Optional[str] = None,
    ) -> bytes:
        if isinstance(value, bytes):
            return value

        if isinstance(value, bytearray):
            return bytes(value)

        self._error(BytesException(name, value, description))
        return bytes()

    @overload
    def check_opt_bytes(
        self,
        name: str,
        value: Any,
        *,
        description: Optional[str] = None,
    ) -> Optional[bytes]:
        ...

    @overload
    def check_opt_bytes(
        self,
        name: str,
        value: Any,
        *,
        default: bytes,
        description: Optional[str] = None,
    ) -> bytes:
        ...

    def check_opt_bytes(
        self,
        name: str,
        value: Any,
        *,
        default: Optional[bytes] = None,
        description: Optional[str] = None,
    ) -> Optional[bytes]:
        if value is None:
            return default

        return self.check_bytes(name, value, description=description)

    def check_bool(
        self,
        name: str,
        value: Any,
        *,
        description: Optional[str] = None,
    ) -> bool:
        if isinstance(value, bool):
            return value

        self._error(BoolException(name, value, description))
        return False

    @overload
    def check_opt_bool(
        self,
        name: str,
        value: Any,
        *,
        description: Optional[str] = None,
    ) -> Optional[bool]:
        ...

    @overload
    def check_opt_bool(
        self,
        name: str,
        value: Any,
        *,
        default: bool,
        description: Optional[str] = None,
    ) -> bool:
        ...

    def check_opt_bool(
        self,
        name: str,
        value: Any,
        *,
        default: Optional[bool] = None,
        description: Optional[str] = None,
    ) -> Optional[bool]:
        if value is None:
            return default

        return self.check_bool(name, value, description=description)

    def check_int(
        self,
        name: str,
        value: Any,
        *,
        description: Optional[str] = None,
    ) -> int:
        if isinstance(value, int):
            return value

        self._error(IntException(name, value, description))
        return -1

    @overload
    def check_opt_int(
        self,
        name: str,
        value: Any,
        *,
        description: Optional[str] = None,
    ) -> Optional[int]:
        ...

    @overload
    def check_opt_int(
        self,
        name: str,
        value: Any,
        *,
        default: int,
        description: Optional[str] = None,
    ) -> int:
        ...

    def check_opt_int(
        self,
        name: str,
        value: Any,
        *,
        default: Optional[int] = None,
        description: Optional[str] = None,
    ) -> Optional[int]:
        if value is None:
            return default

        return self.check_int(name, value, description=description)

    def check_float(
        self,
        name: str,
        value: Any,
        *,
        description: Optional[str] = None,
    ) -> float:
        if isinstance(value, float):
            return value

        self._error(FloatException(name, value, description))
        return -1.0

    @overload
    def check_opt_float(
        self,
        name: str,
        value: Any,
        *,
        description: Optional[str] = None,
    ) -> Optional[float]:
        ...

    @overload
    def check_opt_float(
        self,
        name: str,
        value: Any,
        *,
        default: float,
        description: Optional[str] = None,
    ) -> float:
        ...

    def check_opt_float(
        self,
        name: str,
        value: Any,
        *,
        default: Optional[float] = None,
        description: Optional[str] = None,
    ) -> Optional[float]:
        if value is None:
            return default

        return self.check_float(name, value, description=description)

    def check_sequence(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> Sequence[T]:
        if not isinstance(value, Sequence):
            self._error(SequenceException(name, value, description))
            return []

        value = cast(Sequence[Any], value)

        if of is Any:
            return value

        for i, element in enumerate(value):
            if custom_of_checker is not None:
                if custom_of_checker(element):
                    continue

                # todo: pass in element value, type
                self._error(SequenceOfException(name, value, description))

            is_instance_of, instance_of_desc = self._generic_isinstance(element, of)
            if not is_instance_of:
                self._error(SequenceOfException(name, value, description))

        return value

    @overload
    def check_opt_sequence(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        default_sequence: Callable[[], Sequence[T]] = lambda: [],
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> Sequence[T]:
        ...

    @overload
    def check_opt_sequence(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        default_sequence: Callable[[], Optional[Sequence[T]]] = lambda: None,
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> Optional[Sequence[T]]:
        ...

    def check_opt_sequence(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        default_sequence: Callable[[], Optional[Sequence[T]]] = lambda: [],
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> Optional[Sequence[T]]:
        if value is None:
            return default_sequence()

        self.check_sequence(
            name,
            value,
            of=of,
            custom_of_checker=custom_of_checker,
            description=description,
        )

        return value

    def check_mutable_sequence(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        default_element: Optional[Callable[[], T]] = None,
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> MutableSequence[T]:
        if not isinstance(value, MutableSequence):
            self._error(MutableSequenceException(name, value, description))
            return []

        value = cast(Sequence[Any], value)

        if of is Any:
            return value

        for i, element in enumerate(value):
            if custom_of_checker is not None:
                if custom_of_checker(element):
                    continue

                # todo: pass in element value, type
                self._error(MutableSequenceOfException(name, value, description))

            is_instance_of, instance_of_desc = self._generic_isinstance(element, of)
            if not is_instance_of:
                self._error(MutableSequenceOfException(name, value, description))

            if element is None and default_element is not None:
                value[i] = default_element()

        return value

    @overload
    def check_opt_mutable_sequence(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        default_mutable_sequence: Callable[[], MutableSequence[T]] = lambda: [],
        default_element: Optional[Callable[[], T]] = None,
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> MutableSequence[T]:
        ...

    @overload
    def check_opt_mutable_sequence(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        default_mutable_sequence: Callable[
            [], Optional[MutableSequence[T]]
        ] = lambda: None,
        default_element: Optional[Callable[[], T]] = None,
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> Optional[MutableSequence[T]]:
        ...

    def check_opt_mutable_sequence(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        default_mutable_sequence: Callable[
            [], Optional[MutableSequence[T]]
        ] = lambda: [],
        default_element: Optional[Callable[[], T]] = None,
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> Optional[MutableSequence[T]]:
        if value is None:
            return default_mutable_sequence()

        self.check_mutable_sequence(
            name,
            value,
            of=of,
            default_element=default_element,
            custom_of_checker=custom_of_checker,
            description=description,
        )

        return value

    def check_set(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> Set[T]:
        if not isinstance(value, Set):
            self._error(SetException(name, value, description))
            return set()

        value = cast(Set[Any], value)

        if of is Any:
            return value

        for i, element in enumerate(value):
            if custom_of_checker is not None:
                if custom_of_checker(element):
                    continue

                # todo: pass in element value, type
                self._error(SetOfException(name, value, description))

            is_instance_of, instance_of_desc = self._generic_isinstance(element, of)
            if not is_instance_of:
                self._error(SetOfException(name, value, description))

        return value

    @overload
    def check_opt_set(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        default_set: Callable[[], Set[T]] = lambda: set(),
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> Set[T]:
        ...

    @overload
    def check_opt_set(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        default_set: Callable[[], Optional[Set[T]]] = lambda: None,
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> Optional[Set[T]]:
        ...

    def check_opt_set(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        default_set: Callable[[], Optional[Set[T]]] = lambda: set(),
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> Optional[Set[T]]:
        if value is None:
            return default_set()

        self.check_set(
            name,
            value,
            of=of,
            custom_of_checker=custom_of_checker,
            description=description,
        )

        return value

    def check_mutable_set(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> MutableSet[T]:
        if not isinstance(value, MutableSet):
            self._error(MutableSetException(name, value, description))
            return set()

        self.check_set(
            name,
            value,
            of=of,
            custom_of_checker=custom_of_checker,
            description=description,
        )

        return value

    @overload
    def check_opt_mutable_set(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        default_mutable_set: Callable[[], MutableSet[T]] = lambda: set(),
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> MutableSet[T]:
        ...

    @overload
    def check_opt_mutable_set(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        default_mutable_set: Callable[[], Optional[MutableSet[T]]] = lambda: None,
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> Optional[MutableSet[T]]:
        ...

    def check_opt_mutable_set(
        self,
        name: str,
        value: Any,
        *,
        of: Type[T] = Any,
        default_mutable_set: Callable[[], Optional[MutableSet[T]]] = lambda: set(),
        custom_of_checker: Optional[Callable[[Any], bool]] = None,
        description: Optional[str] = None,
    ) -> Optional[MutableSet[T]]:
        if value is None:
            return default_mutable_set()

        self.check_mutable_set(
            name,
            value,
            of=of,
            custom_of_checker=custom_of_checker,
            description=description,
        )

        return value

    def check_mapping(
        self,
        name: str,
        value: Any,
        *,
        keys_of: Type[KT] = Type[Any],
        values_of: Type[VT] = Any,
        description: Optional[str] = None,
    ) -> Mapping[KT, VT]:
        if not isinstance(value, Mapping):
            self._error(MappingException(name, value, description))
            return {}

        if keys_of is not Any:
            self.check_sequence(f"keys of {name}", list(value.keys()), of=keys_of)

        if values_of is not Any:
            self.check_sequence(f"values of {name}", list(value.values()), of=values_of)

        return cast(Mapping[KT, VT], value)

    @overload
    def check_opt_mapping(
        self,
        name: str,
        value: Any,
        *,
        default_mapping: Callable[[], Mapping[KT, VT]] = lambda: {},
        keys_of: Type[KT] = Any,
        values_of: Type[VT] = Any,
        description: Optional[str] = None,
    ) -> Mapping[KT, VT]:
        ...

    @overload
    def check_opt_mapping(
        self,
        name: str,
        value: Any,
        *,
        default_mapping: Callable[[], Optional[Mapping[KT, VT]]] = lambda: None,
        keys_of: Type[KT] = Any,
        values_of: Type[VT] = Any,
        description: Optional[str] = None,
    ) -> Optional[Mapping[KT, VT]]:
        ...

    def check_opt_mapping(
        self,
        name: str,
        value: Any,
        *,
        default_mapping: Callable[[], Optional[Mapping[KT, VT]]] = lambda: {},
        keys_of: Type[KT] = Any,
        values_of: Type[VT] = Any,
        description: Optional[str] = None,
    ) -> Optional[Mapping[KT, VT]]:
        if value is None:
            return default_mapping()

        self.check_mapping(
            name,
            value,
            keys_of=keys_of,
            values_of=values_of,
            description=description,
        )

        return value

    def check_mutable_mapping(
        self,
        name: str,
        value: Any,
        *,
        keys_of: Type[KT] = Any,
        values_of: Type[VT] = Any,
        description: Optional[str] = None,
    ) -> MutableMapping[KT, VT]:
        if not isinstance(value, MutableMapping):
            self._error(MutableMappingException(name, value, description))
            return {}

        self.check_mapping(
            name,
            value,
            keys_of=keys_of,
            values_of=values_of,
            description=description,
        )

        return value

    @overload
    def check_opt_mutable_mapping(
        self,
        name: str,
        value: Any,
        *,
        keys_of: Type[KT] = Any,
        values_of: Type[VT] = Any,
        default_mutable_mapping: Callable[[], MutableMapping[KT, VT]] = lambda: {},
        description: Optional[str] = None,
    ) -> MutableMapping[KT, VT]:
        ...

    @overload
    def check_opt_mutable_mapping(
        self,
        name: str,
        value: Any,
        *,
        keys_of: Type[KT] = Any,
        values_of: Type[VT] = Any,
        default_mutable_mapping: Callable[
            [],
            Optional[MutableMapping[KT, VT]],
        ] = lambda: None,
        description: Optional[str] = None,
    ) -> Optional[MutableMapping[KT, VT]]:
        ...

    def check_opt_mutable_mapping(
        self,
        name: str,
        value: Any,
        *,
        keys_of: Type[KT] = Any,
        values_of: Type[VT] = Any,
        default_mutable_mapping: Callable[
            [],
            Optional[MutableMapping[KT, VT]],
        ] = lambda: {},
        description: Optional[str] = None,
    ) -> Optional[MutableMapping[KT, VT]]:
        if value is None:
            return default_mutable_mapping()

        self.check_opt_mapping(
            name,
            value,
            keys_of=keys_of,
            values_of=values_of,
            description=description,
        )

        return value

    # this isn't really a property, just so it's easier to call
    @property
    def check_all(self):
        self._enable_suppress_and_record()
        return CheckAll(check_instance=self)


# r = Check(suppress_and_record=False)

# # seq = r.check_opt_sequence("my seq", [])

# # my_sq = r.check_sequence("my seq", [None, [1, "hello",]], of=Optional[Sequence[Union[int, str]]])
# # print(my_sq)

# with r.check_all:
#     a = r.check_str("str_a", 1.2, description="My first string")
#     b = r.check_int("str_b", "b", description="My second string")
#     c = r.check_sequence("my sq", 1)

# print(a, b)
