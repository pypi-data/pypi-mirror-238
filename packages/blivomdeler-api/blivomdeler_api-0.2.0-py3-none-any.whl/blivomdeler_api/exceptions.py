# Other
class InternalAPIException(Exception):
    pass


class UserError(Exception):
    pass


# User errors
class InvalidCredentialsError(UserError):
    pass


class LoginRequiredError(UserError):
    pass


# Internal exceptions
class InvalidResponseException(InternalAPIException):
    pass
