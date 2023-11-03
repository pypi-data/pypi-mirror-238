import os
from pathlib import Path
from typing import Optional

_ATOTI_JAVA_HOME_ENV_VAR_NAME = "ATOTI_JAVA_HOME"
_JAVA_HOME_ENV_VAR_NAME = "JAVA_HOME"


def _get_java_home() -> Optional[Path]:
    atoti_java_home = os.environ.get(_ATOTI_JAVA_HOME_ENV_VAR_NAME)
    if atoti_java_home:
        return Path(atoti_java_home)
    try:
        from jdk4py import JAVA_HOME  # pylint:disable=nested-import
    except ImportError:
        java_home = os.environ.get(_JAVA_HOME_ENV_VAR_NAME)
        return Path(java_home) if java_home else None
    else:
        return JAVA_HOME


def get_java_executable_path(*, executable_name: str = "java") -> Path:
    java_home = _get_java_home()
    return java_home / "bin" / executable_name if java_home else Path(executable_name)
