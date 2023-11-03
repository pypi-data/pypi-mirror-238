from starlette.authentication import AuthCredentials
from starlette.authentication import AuthenticationBackend
from starlette.authentication import BaseUser
from starlette.authentication import UnauthenticatedUser
from starlette.requests import HTTPConnection


class AuthenticationInfo:
    credentials: AuthCredentials
    user: BaseUser

    def __init__(
        self,
        credentials: AuthCredentials | None = None,
        user: BaseUser | None = None,
    ):
        self.credentials = credentials or AuthCredentials(['authenticated'])
        self.user = user or UnauthenticatedUser()


class AmsdalAuthenticationBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> tuple[AuthCredentials, BaseUser] | None:
        from amsdal_utils.lifecycle.enum import LifecycleEvent
        from amsdal_utils.lifecycle.producer import LifecycleProducer

        if 'Authorization' not in conn.headers:
            return None

        auth = conn.headers['Authorization']
        authentication_info = AuthenticationInfo()

        LifecycleProducer.publish(
            LifecycleEvent.ON_AUTHENTICATE,
            auth_header=auth,
            authentication_info=authentication_info,
        )

        return authentication_info.credentials, authentication_info.user
