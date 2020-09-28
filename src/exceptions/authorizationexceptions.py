from baseexceptions import AuthorizationError


class InvalidRequest(AuthorizationError):
    def __init__(self, **kwargs):
        super().__init__(
            error='invalid_request', 
            **kwargs
        )


class UnauthorizedClient(AuthorizationError):
    def __init__(self, **kwargs):
        super().__init__(
            error='unauthorized_client', 
            **kwargs
        )


class AccessDenied(AuthorizationError):
    def __init__(self, **kwargs):
        super().__init__(
            error='access_denied', 
            **kwargs
        )


class UnsupportedResponseType(AuthorizationError):
    def __init__(self, **kwargs):
        super().__init__(
            error='unsupported_response_type', 
            **kwargs
        )


class InvalidScope(AuthorizationError):
    def __init__(self, **kwargs):
        super().__init__(
            error='invalid_scope', 
            **kwargs
        )


class ServerError(AuthorizationError):
    def __init__(self, **kwargs):
        super().__init__(
            error='server_error', 
            **kwargs
        )


class TemporarilyUnavailable(AuthorizationError):
    def __init__(self, **kwargs):
        super().__init__(
            error='temporarily_unavailable', 
           **kwargs
        )

