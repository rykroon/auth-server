class OAuthError(Exception):
    def __init__(self, error, error_description=None, status_code=400):
        self.error = error
        self.error_description = error_description
        self.status_code = status_code


class InvalidRequest(OAuthError):
    def __init__(self, error_description=None):
        super().__init__(
            error='invalid_request', 
            error_description=error_description
        )


class InvalidClient(OAuthError):
    def __init__(self, error_description=None):
        super().__init__(
            error='invalid_client', 
            error_description=error_description,
            status_code=401
        )


class InvalidGrant(OAuthError):
    def __init__(self, error_description=None):
        super().__init__(
            error='invalid_grant', 
            error_description=error_description
        )


class InvalidScope(OAuthError):
    def __init__(self, error_description=None):
        super().__init__(
            error='invalid_scope', 
            error_description=error_description
        )


class UnauthorizedClient(OAuthError):
    def __init__(self, error_description=None):
        super().__init__(
            error='unauthorized_client', 
            error_description=error_description
        )


class UnsupportedGrantType(OAuthError):
    def __init__(self, error_description=None):
        super().__init__(
            error='unsupported_grant_type', 
            error_description=error_description
        )




