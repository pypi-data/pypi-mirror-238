DEFAULT_STATUS_CODE = 400


def vader_exception_handler(exception):
    return {
        "message": str(exception.message),
        "status": exception.status_code,
        "details": exception.details,
    }, exception.status_code


class VaderCommonError(Exception):
    def __init__(
        self, message: str, details: str = "", status_code: int = DEFAULT_STATUS_CODE
    ):
        self.message = message
        self.details = details
        self.status_code = status_code
        super().__init__(self.message)


class VaderConfigError(VaderCommonError):
    """Bad Configuration passed to Vader"""


class VaderUnauthorizedError(VaderCommonError):
    """Unauthorized request to a project"""


class VaderMongoError(VaderCommonError):
    """Error with Mongo"""


class VaderVaultError(VaderCommonError):
    """Error with Vault"""


class VaderNotFoundError(VaderCommonError):
    """Resource not found in Vader"""


class VaderGenericError(VaderCommonError):
    """Unauthorized request to a project"""
