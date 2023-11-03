from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Optional

from atoti_core import keyword_only_dataclass
from typing_extensions import override

from .._config import Config, pop_optional_sub_config
from .basic_authentication_config import BasicAuthenticationConfig
from .kerberos_config import KerberosConfig
from .ldap_config import LdapConfig
from .oidc_config import OidcConfig


@keyword_only_dataclass
@dataclass(frozen=True)
class AuthenticationConfig(Config):
    """The configuration of the authentication mechanism used by the server to know which users are allowed to connect to the application and which roles they are granted.

    Note:
       This feature is not part of the community edition: it needs to be `unlocked <../../how_tos/unlock_all_features.html>`__.

    If any non-:class:`basic <atoti.BasicAuthenticationConfig>` authentication is configured, basic authentication will be automatically enabled as well to make it easier to create service/technical users.

    Roles and restrictions can be configured using :attr:`~atoti.Session.security`.
    """

    basic: Optional[BasicAuthenticationConfig] = None
    kerberos: Optional[KerberosConfig] = None
    ldap: Optional[LdapConfig] = None
    oidc: Optional[OidcConfig] = None

    @classmethod
    @override
    def _from_mapping(cls, mapping: Mapping[str, Any]) -> AuthenticationConfig:
        data = dict(mapping)
        return cls(
            basic=pop_optional_sub_config(
                data, attribute_name="basic", sub_config_class=BasicAuthenticationConfig
            ),
            kerberos=pop_optional_sub_config(
                data, attribute_name="kerberos", sub_config_class=KerberosConfig
            ),
            ldap=pop_optional_sub_config(
                data, attribute_name="ldap", sub_config_class=LdapConfig
            ),
            oidc=pop_optional_sub_config(
                data, attribute_name="oidc", sub_config_class=OidcConfig
            ),
            **data,
        )

    def __post_init__(self) -> None:
        assert (
            len([value for value in self.__dict__.values() if value is not None]) == 1
        ), "One and only one authentication mechanism can be configured."
