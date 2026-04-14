from typing import Dict
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from models import Decision


class TokenBucketRateLimiter:
    """Per-customer token bucket rate limiter with on-demand refill.
    
    Each customer gets a bucket of tokens that refill continuously based on elapsed time.
    Requests consume 1 token. When tokens are exhausted, requests are denied.
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        """Initialize the rate limiter.
        
        Args:
            capacity: Maximum tokens per customer (e.g., 100).
            refill_rate: Tokens added per second (e.g., 10).
        """
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.buckets: Dict[str, float] = {}  # customer_id → token count
        self.last_refill: Dict[str, int] = {}  # customer_id → timestamp (ms)

    def check(self, customer_id: str, current_time_ms: int) -> Decision:
        """Check if a request is allowed for the given customer.
        
        Args:
            customer_id: Unique identifier for the customer.
            current_time_ms: Current time in milliseconds (for testing and refill calculation).
        
        Returns:
            Decision object with allowed status, remaining tokens, and retry time.
        """
        # FIX #1: Initialize bucket at FULL capacity, not empty
        if customer_id not in self.buckets:
            self.buckets[customer_id] = self.capacity
            self.last_refill[customer_id] = current_time_ms

        # Calculate elapsed time and refill tokens based on elapsed time
        elapsed_ms = current_time_ms - self.last_refill[customer_id]
        tokens_to_add = (elapsed_ms / 1000.0) * self.refill_rate
        self.buckets[customer_id] += tokens_to_add

        # FIX #2: Cap tokens at capacity
        self.buckets[customer_id] = min(self.buckets[customer_id], self.capacity)

        # Update last refill timestamp
        self.last_refill[customer_id] = current_time_ms

        current = self.buckets[customer_id]

        # Allow request if we have at least 1 token
        if current >= 1:
            self.buckets[customer_id] = current - 1
            return Decision(
                allowed=True,
                remaining=int(current - 1),
                retry_after_ms=0
            )
        else:
            # Deny request and calculate wait time
            tokens_needed = 1.0 - current
            retry_after_seconds = tokens_needed / self.refill_rate

            # FIX #3: Convert seconds to milliseconds (multiply by 1000)
            retry_after_ms = int(retry_after_seconds * 1000)

            return Decision(
                allowed=False,
                remaining=0,
                retry_after_ms=retry_after_ms
            )
