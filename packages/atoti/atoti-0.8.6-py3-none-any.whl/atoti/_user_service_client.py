from pathlib import Path
from typing import Optional

from atoti_core import BaseCubesBound, BaseSession, deprecated
from atoti_query import Auth, ClientCertificate, QuerySession
from atoti_query._internal import Security


class UserServiceClient:
    @classmethod
    def from_session(
        cls, session: BaseSession[BaseCubesBound, Security], /
    ) -> Security:
        deprecated("`UserServiceClient` is deprecated, use `Session.security` instead.")
        return session._security

    @classmethod
    def from_url(
        cls,
        url: str,
        /,
        *,
        auth: Optional[Auth] = None,
        certificate_authority: Optional[Path] = None,
        client_certificate: Optional[ClientCertificate] = None,
    ) -> Security:
        session = QuerySession(
            url,
            auth=auth,
            certificate_authority=certificate_authority,
            client_certificate=client_certificate,
        )
        return cls.from_session(session)
