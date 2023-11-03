from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal, Optional, Union

from atoti_core import keyword_only_dataclass

from .._config import Config


@keyword_only_dataclass
@dataclass(frozen=True)
class OidcConfig(Config):
    """The configuration to connect to an `OpenID Connect <https://openid.net/connect/>`__ authentication provider (Auth0, Google, Keycloak, etc.).

    The user's roles are defined using :attr:`atoti_query.security.Security.oidc` and :attr:`~atoti_query.security.Security.individual_roles`.

    Example:
        >>> auth_config = tt.OidcConfig(
        ...     provider_id="auth0",
        ...     issuer_url="https://example.auth0.com",
        ...     client_id="some client ID",
        ...     client_secret="some client secret",
        ...     name_claim="email",
        ...     scopes=["email", "profile"],
        ...     roles_claims=[
        ...         "https://example.com/roles",
        ...         ["other", "path", "to", "roles"],
        ...     ],
        ... )

    """

    provider_id: str
    """The name of the provider.

    It is used to build the redirect URL: ``f"{session_url}/login/oauth2/code/{provider_id}"``.
    """

    issuer_url: str
    """The issuer URL parameter from the provider's OpenID Connect configuration endpoint."""

    client_id: str
    """The app's client ID, obtained from the authentication provider."""

    client_secret: str
    """The app's client secret, obtained from the authentication provider."""

    use_client_secret_as_certificate: bool = False
    """If ``True``, the passed :attr:`client_secret` must be a client certificate instead of a random secret.
    This client certificate will be passed in the ``X-Cert`` header of the request made to the OIDC provider to retrieve an access token.
    """

    name_claim: Optional[str] = None
    """The name of the claim in the ID token to use as the name of the user."""

    roles_claims: Iterable[Union[str, Iterable[str]]] = ()
    """The claims of the ID token from which to extract roles to use as keys in the :attr:`~atoti_query.security.oidc_security.OidcSecurity.role_mapping`.

    When the elements of the sequence are also sequences, the inner elements will be used as a path pointing to a nested value in the token.
    """

    scopes: Iterable[str] = ()
    """The scopes to request from the authentication provider."""

    access_token_format: Literal["jwt", "opaque"] = "jwt"
    """The format of the access tokens delivered by the OIDC provider.

    Opaque tokens involve another request to the OIDC provider's user info endpoint to retrieve the user details.
    The URL of this user info endpoint will be fetched from the ``f"{issuer_url}/.well-known/openid-configuration"`` endpoint.

    See also:
        Opaque tokens can be used with :class:`atoti_query.OAuth2ResourceOwnerPasswordAuthentication`.
    """

    def __post_init__(self) -> None:
        self.__dict__["roles_claims"] = [
            [role_claim] if isinstance(role_claim, str) else role_claim
            for role_claim in self.roles_claims
        ]
