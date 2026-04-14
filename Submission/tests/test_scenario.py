import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import TokenBucketRateLimiter


class TestInitialization:
    def test_first_request_has_full_capacity(self) -> None:
        limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10)
        result = limiter.check("user1", 0)
        assert result.allowed is True
        assert result.remaining == 99


class TestBasicRateLimiting:
    def test_allow_within_capacity(self) -> None:
        limiter = TokenBucketRateLimiter(capacity=5, refill_rate=10)
        for i in range(5):
            result = limiter.check("user1", 0)
            assert result.allowed is True
        
        result = limiter.check("user1", 0)
        assert result.allowed is False
        assert result.remaining == 0


class TestRefillMechanism:
    def test_refill_calculation(self) -> None:
        limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10)
        
        for i in range(60):
            limiter.check("user1", 0)
        
        result = limiter.check("user1", 2000)
        assert result.allowed is True
        assert result.remaining == 59


class TestMultipleCustomers:
    def test_independent_quotas(self) -> None:
        limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10)
        
        for i in range(50):
            limiter.check("customer1", 0)
        
        for i in range(20):
            limiter.check("customer2", 0)
        
        result1 = limiter.check("customer1", 0)
        assert result1.remaining == 49
        
        result2 = limiter.check("customer2", 0)
        assert result2.remaining == 79


class TestSpecExample:
    def test_full_scenario_end_to_end(self) -> None:
        limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10)
        
        # T=0: First request, 100 available
        result = limiter.check("user1", 0)
        assert result.allowed is True
        
        # T=0: 59 more requests (60 total consumed)
        for i in range(59):
            limiter.check("user1", 0)
        # Remaining: 40
        
        # T=2000ms: Refill (40 + 20 = 60)
        result = limiter.check("user1", 2000)
        assert result.allowed is True
        assert result.remaining == 59
        
        # T=2000ms: 59 more requests (10 denied out of 70)
        allowed, denied = 0, 0
        for i in range(69):
            result = limiter.check("user1", 2000)
            if result.allowed:
                allowed += 1
            else:
                denied += 1
        assert allowed == 59 and denied == 10
        
        # T=7000ms: Refill (50 tokens)
        result = limiter.check("user1", 7000)
        assert result.allowed is True
        
        # T=7000ms: 29 more requests all allowed
        for i in range(29):
            limiter.check("user1", 7000)
        # Remaining: 20
        
        # T=17000ms: Refill capped at 100
        result = limiter.check("user1", 17000)
        assert result.allowed is True
        
        # T=17000ms: 79 more requests all allowed
        for i in range(79):
            limiter.check("user1", 17000)
