from baseexceptions import TokenError


class InvalidRequest(TokenError):
    def __init__(self, **kwargs):
        super().__init__(
            error='invalid_request',
            **kwargs
        )


class InvalidClient(TokenError):
    def __init__(self, **kwargs):
        super().__init__(
            error='invalid_client', 
            status_code=401,
            **kwargs
        )


class InvalidGrant(TokenError):
    def __init__(self, **kwargs):
        super().__init__(
            error='invalid_grant', 
            **kwargs
        )


class UnauthorizedClient(TokenError):
    def __init__(self, **kwargs):
        super().__init__(
            error='unauthorized_client', 
            **kwargs
        )


class UsupportedGrantType(TokenError):
    def __init__(self, **kwargs):
        super().__init__(
            error='unsupported_grant_type', 
            **kwargs
        )


class invalid_scope(TokenError):
    def __init__(self, **kwargs):
        super().__init__(
            error='invalid_scope', 
            **kwargs
        )

        