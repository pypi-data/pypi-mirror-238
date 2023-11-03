class KoppeltaalApiError(Exception):
    """Base exception class for Koppeltaal errors."""

    ...


class OAuthError(Exception):
    """Base exception class for oauth errors."""

    ...


class GetAccessTokenError(OAuthError):
    pass


class AuthorizeError(OAuthError):
    pass
