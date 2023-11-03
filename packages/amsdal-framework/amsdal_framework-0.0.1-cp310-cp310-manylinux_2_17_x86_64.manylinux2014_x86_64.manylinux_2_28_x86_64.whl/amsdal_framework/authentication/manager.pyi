from amsdal_framework.authentication.enums import AuthType as AuthType
from amsdal_framework.authentication.handlers.base import AuthHandlerBase as AuthHandlerBase
from amsdal_framework.authentication.handlers.credentials import CredentialsAuthHandler as CredentialsAuthHandler
from amsdal_framework.authentication.handlers.token import TokenAuthHandler as TokenAuthHandler
from amsdal_framework.configs.main import settings as settings
from amsdal_framework.errors import AmsdalAuthenticationError as AmsdalAuthenticationError, AmsdalMissingCredentialsError as AmsdalMissingCredentialsError
from amsdal_utils.utils.singleton import Singleton

class AuthManager(metaclass=Singleton):
    _auth_handler: AuthHandlerBase
    def __init__(self, auth_type: AuthType | None = ...) -> None: ...
    def authenticate(self) -> None: ...
