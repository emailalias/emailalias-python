class EmailAliasError(Exception):
    """Base exception. `status` is the HTTP code, `message` the server detail."""

    def __init__(self, message: str, status: int = 0):
        super().__init__(message)
        self.status = status
        self.message = message


class AuthenticationError(EmailAliasError):
    """401 — invalid API key, or the key's owner is no longer Premium."""


class NotFoundError(EmailAliasError):
    """404."""


class RateLimitError(EmailAliasError):
    """429. Honour the `X-RateLimit-Reset` header before retrying."""
