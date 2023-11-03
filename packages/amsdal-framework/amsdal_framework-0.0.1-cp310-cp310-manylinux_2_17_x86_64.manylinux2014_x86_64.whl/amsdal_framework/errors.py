from amsdal_utils.errors import AmsdalError


class AmsdalRuntimeError(AmsdalError):
    ...


class TransactionNotFoundError(AmsdalError):
    ...


class AmsdalAuthenticationError(AmsdalRuntimeError):
    ...


class AmsdalMissingCredentialsError(AmsdalAuthenticationError):
    ...
