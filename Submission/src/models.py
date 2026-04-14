from dataclasses import dataclass


@dataclass
class Decision:
    """Result of a rate limit check.
    
    Attributes:
        allowed: Whether the request is allowed to proceed.
        remaining: Number of tokens remaining in the bucket (0 if denied).
        retry_after_ms: Time in milliseconds to wait before retrying (0 if allowed).
    """
    allowed: bool
    remaining: int
    retry_after_ms: int
