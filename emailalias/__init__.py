from .client import Client
from .errors import EmailAliasError, AuthenticationError, RateLimitError, NotFoundError

__all__ = [
    "Client",
    "EmailAliasError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
]
__version__ = "0.1.0"
