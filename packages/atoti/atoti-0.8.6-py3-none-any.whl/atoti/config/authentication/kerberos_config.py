from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from atoti_core import keyword_only_dataclass

from .._config import Config, convert_path_to_absolute_string


@keyword_only_dataclass
@dataclass(frozen=True)
class KerberosConfig(Config):
    """The configuration to connect to a `Kerberos <https://web.mit.edu/kerberos/>`__ authentication provider.

    The user's roles can be defined using :attr:`atoti_query.security.Security.kerberos` and :attr:`~atoti_query.security.Security.individual_roles`.

    Example:
        >>> auth_config = tt.KerberosConfig(
        ...     service_principal="HTTP/localhost",
        ...     keytab="config/example.keytab",
        ...     krb5_config="config/example.krb5",
        ... )
    """

    service_principal: str
    """The principal that the Atoti application will use."""

    keytab: Optional[Union[Path, str]] = None
    """The path to the keytab file to use."""

    krb5_config: Optional[Union[Path, str]] = None
    """The path to the Kerberos config file.

    Defaults to the OS-specific default location.
    """

    def __post_init__(self) -> None:
        convert_path_to_absolute_string(self, "keytab", "krb5_config")
