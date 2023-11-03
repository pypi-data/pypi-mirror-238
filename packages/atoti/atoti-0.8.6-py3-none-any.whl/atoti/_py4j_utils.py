import datetime
from collections.abc import Collection, Iterable, Mapping
from typing import Any, Optional, Union, cast

import pandas as pd
from atoti_core import ColumnIdentifier, DataType
from py4j.java_collections import JavaArray, JavaMap, ListConverter
from py4j.java_gateway import CallbackServer, JavaClass, JavaGateway, JavaObject

from .type import FLOAT_ARRAY, INT_ARRAY


# No type stubs for py4j, so we ignore this error
def to_java_object_array(
    collection: Collection[Any],
    *,
    gateway: JavaGateway,
) -> JavaArray:
    """Transform the Python collection into a Java array."""
    return to_typed_java_array(
        collection, gateway=gateway, array_type=gateway.jvm.Object
    )


def to_java_map(
    mapping: Mapping[Any, Any],
    *,
    gateway: JavaGateway,
) -> JavaMap:
    """Convert a Python mapping to a JavaMap preserving the order of the keys."""
    return _to_typed_java_map(mapping, gateway=gateway, clazz="java.util.LinkedHashMap")


def to_java_object_map(
    mapping: Mapping[Any, Any],
    *,
    gateway: JavaGateway,
) -> JavaMap:
    """Convert a Python mapping to a JavaMap preserving the order of the keys."""
    return to_java_map(
        {
            as_java_object(key, gateway=gateway): as_java_object(value, gateway=gateway)
            for key, value in mapping.items()
        },
        gateway=gateway,
    )


def _to_typed_java_map(
    to_convert: Mapping[Any, Any],
    *,
    clazz: str,
    gateway: JavaGateway,
) -> JavaMap:
    """Convert to a map of the given type."""
    map_type = JavaClass(clazz, gateway._gateway_client)
    java_map = cast(JavaMap, map_type())
    for key in to_convert:
        java_map[key] = as_java_object(to_convert[key], gateway=gateway)
    return java_map


def to_java_string_array(
    collection: Collection[str],
    *,
    gateway: JavaGateway,
) -> JavaArray:
    """Transform the Python collection into a Java array of strings."""
    return to_typed_java_array(
        collection, gateway=gateway, array_type=gateway.jvm.String
    )


def to_java_object_list(
    iterable: Iterable[Any],
    *,
    gateway: JavaGateway,
) -> Any:
    """Transform the Python iterable into a Java list of object."""
    return ListConverter().convert(
        [as_java_object(e, gateway=gateway) for e in iterable], gateway._gateway_client
    )


def to_typed_java_array(
    collection: Collection[Any],
    *,
    array_type: object,
    gateway: JavaGateway,
) -> JavaArray:
    """Transform to Java array of given type."""
    array = cast(JavaArray, gateway.new_array(array_type, len(collection)))
    if collection:
        for index, elem in enumerate(collection):
            array[index] = as_java_object(elem, gateway=gateway)
    return array


def to_java_date_or_time(
    date: Union[datetime.date, datetime.datetime, datetime.time],
    *,
    gateway: JavaGateway,
) -> JavaObject:
    """Transform the Python date into a Java one."""
    jvm: Any = gateway.jvm
    if isinstance(date, datetime.datetime):
        if not date.tzinfo:
            return jvm.java.time.LocalDateTime.parse(date.isoformat())
        return jvm.java.time.ZonedDateTime.parse(date.isoformat())
    if isinstance(date, datetime.time):
        if date.tzinfo:
            raise ValueError(
                f"Cannot handle time with timezone information: `{date.tzinfo}`."
            )
        return jvm.java.time.LocalTime.of(
            date.hour,
            date.minute,
            date.second,
            date.microsecond * 1000,
        )
    return jvm.java.time.LocalDate.of(date.year, date.month, date.day)


def to_qfs_vector(
    arg: Collection[Any],
    *,
    data_type: Optional[DataType] = None,
    gateway: JavaGateway,
) -> Any:
    jvm: Any = gateway.jvm
    vector_package = jvm.com.qfs.vector.array.impl
    if all(isinstance(x, int) for x in arg):
        if data_type == INT_ARRAY:
            array = to_typed_java_array(
                arg, gateway=gateway, array_type=gateway.jvm.int
            )
            return vector_package.ArrayIntegerVector(array)
        array = to_typed_java_array(arg, gateway=gateway, array_type=gateway.jvm.long)
        return vector_package.ArrayLongVector(array)
    if all(isinstance(x, (float, int)) for x in arg):
        if data_type == FLOAT_ARRAY:
            array = to_typed_java_array(
                [float(x) for x in arg],
                gateway=gateway,
                array_type=gateway.jvm.float,
            )
            return vector_package.ArrayFloatVector(array)
        array = to_typed_java_array(
            [float(x) for x in arg], gateway=gateway, array_type=gateway.jvm.double
        )
        return vector_package.ArrayDoubleVector(array)
    array = to_java_object_array(arg, gateway=gateway)
    return vector_package.ArrayObjectVector(array)


def as_java_object(
    arg: Any,
    *,
    gateway: JavaGateway,
    data_type: Optional[DataType] = None,
) -> Any:
    if isinstance(arg, (datetime.date, datetime.datetime, datetime.time)):
        return to_java_date_or_time(arg, gateway=gateway)
    if isinstance(arg, ColumnIdentifier):
        return to_store_field(arg, gateway=gateway)
    if isinstance(arg, tuple):
        return to_qfs_vector(arg, gateway=gateway, data_type=data_type)
    return arg


def to_python_object(
    value: Optional[Any],
    /,
) -> Any:
    if value is None or not isinstance(value, JavaObject):
        return value

    _value: Any = value
    if _value.getClass().getName() in [
        "java.time.LocalDateTime",
        "java.time.ZonedDateTime",
    ]:
        return pd.to_datetime(
            _value.toString()
        ).to_pydatetime()  # spell-checker: disable-line
    if _value.getClass().getName() == "java.time.LocalDate":
        return datetime.date.fromisoformat(_value.toString())
    if _value.getClass().getName() == "java.time.LocalTime":
        return datetime.time.fromisoformat(_value.toString())
    raise TypeError(f"Cannot convert object of type {type(value)} to Python.")


def to_python_dict(
    java_map: JavaMap,
) -> dict[Any, Any]:
    """Convert a Java map to a Python dict."""
    return {key: java_map[key] for key in cast(Any, java_map).keySet().toArray()}


def to_python_list(
    list_to_convert: JavaObject,
) -> list[Any]:
    """Convert a Java list to a Python list."""
    # ignore types when calling a Java function
    return list(cast(Any, list_to_convert).toArray())


def to_store_field(
    identifier: ColumnIdentifier,
    /,
    *,
    gateway: JavaGateway,
) -> Any:
    jvm: Any = gateway.jvm
    StoreField: Any = jvm.com.activeviam.database.api.schema.StoreField  # noqa: N806
    return StoreField(identifier.table_identifier.table_name, identifier.column_name)


def patch_databricks_py4j() -> None:
    """Fix Databricks' monkey patching of py4j."""
    # The problematic version of Databricks outputs:
    # >>> print(CallbackServer.start.__qualname__)
    #  _daemonize_callback_server.<locals>.start
    #
    # More generally, it looks like most local monkey patches will have
    # the "locals" string in their name, so it's worth checking.

    if "locals" in CallbackServer.start.__qualname__:
        databricks_start = CallbackServer.start

        # Re-define the start function, adding back the missing code.
        def start(self: Any) -> None:
            databricks_start(self)

            if not hasattr(self, "_listening_address"):
                info = self.server_socket.getsockname()
                self._listening_address = info[0]
                self._listening_port = info[1]

        CallbackServer.start = start
