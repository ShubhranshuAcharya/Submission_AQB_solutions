import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import TokenBucketRateLimiter


class TestCapacityCap:
    def test_cap_at_max_after_long_idle(self) -> None:
        limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10)
        
        for i in range(100):
            limiter.check("user1", 0)
        
        result = limiter.check("user1", 20000)
        assert result.allowed is True
        
        for i in range(99):
            limiter.check("user1", 20000)
        
        result = limiter.check("user1", 20000)
        assert result.allowed is False


class TestRetryAfterMs:
    def test_retry_in_milliseconds(self) -> None:
        limiter = TokenBucketRateLimiter(capacity=1, refill_rate=10)
        limiter.check("user1", 0)
        
        result = limiter.check("user1", 0)
        assert result.allowed is False
        assert result.retry_after_ms == 100
    
    def test_retry_conversion_1sec(self) -> None:
        limiter = TokenBucketRateLimiter(capacity=1, refill_rate=1)
        limiter.check("user1", 0)
        
        result = limiter.check("user1", 0)
        assert result.allowed is False
        assert result.retry_after_ms == 1000


class TestEdgeCases:
    def test_fractional_token_precision(self) -> None:
        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=3)
        
        for i in range(9):
            limiter.check("user1", 0)
        
        result = limiter.check("user1", 500)
        assert result.allowed is True
        assert result.allowed is True
    
    def test_empty_bucket_reject(self) -> None:
        limiter = TokenBucketRateLimiter(capacity=1, refill_rate=10)
        
        result = limiter.check("user1", 0)
        assert result.allowed is True
        assert result.remaining == 0
        
        result = limiter.check("user1", 0)
        assert result.allowed is False
