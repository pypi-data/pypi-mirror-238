from functools import wraps
from typing import Callable, TypeVar

from typeguard import _CallMemo, check_argument_types
from typing_extensions import ParamSpec

DISABLE_TYPECHECKING_ENV_VAR_NAME = "_ATOTI_DISABLE_TYPECHECKING"

_P = ParamSpec("_P")
_R = TypeVar("_R")


def typecheck(function: Callable[_P, _R], /) -> Callable[_P, _R]:
    @wraps(function)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        memo = _CallMemo(func=function, args=args, kwargs=kwargs)
        check_argument_types(memo)
        return function(*args, **kwargs)

    return wrapper
