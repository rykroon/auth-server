class OAuthError(Exception):
    def to_dict(self):
        raise NotImplementedError


class AuthorizationError(OAuthError):
    def __init__(self, error, error_description=None, error_uri=None, state=None, redirect_uri=None):
        self.error = error
        self.error_description = error_description
        self.error_uri = error_uri
        self.state = state
        self.redirect_uri = redirect_uri

    def to_dict(self):
        result = {
            "error": self.error
        }

        if self.error_description is not None:
            result['error_description'] = self.error_description

        if self. error_uri is not None:
            result['error_uri'] = self.error_uri

        if self.state is not None:
            result['state'] = self.state

        return result


class TokenError(OAuthError):
    def __init__(self, error, error_description=None, error_uri=None, status_code=400):
        self.error = error
        self.error_description = error_description
        self.error_uri = error_uri
        self.status_code = status_code

    def to_dict(self):
        result = {
            "error": self.error
        }

        if self.error_description is not None:
            result['error_description'] = self.error_description

        if self. error_uri is not None:
            result['error_uri'] = self.error_uri

        return result

