import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import TokenBucketRateLimiter


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def demo_basic():
    print_section("Demo 1: Basic Rate Limiting")
    limiter = TokenBucketRateLimiter(capacity=10, refill_rate=2)
    
    print("\nScenario: 10 token capacity, 2 tokens/sec refill rate")
    print("\nT=0ms: Making 5 requests")
    for i in range(5):
        result = limiter.check("user123", 0)
        print(f"  Request {i+1}: {'ALLOWED' if result.allowed else 'DENIED':8} | Remaining: {result.remaining}")
    
    print("\nT=0ms: Trying 6 more requests (should fail at some point)")
    for i in range(6):
        result = limiter.check("user123", 0)
        if result.allowed:
            print(f"  Request {5+i+1}: ALLOWED | Remaining: {result.remaining}")
        else:
            print(f"  Request {5+i+1}: DENIED  | Retry after: {result.retry_after_ms}ms")


def demo_refill():
    print_section("Demo 2: Token Refill Over Time")
    limiter = TokenBucketRateLimiter(capacity=20, refill_rate=5)
    
    print("\nScenario: 20 capacity, 5 tokens/sec")
    print("\nT=0ms: Consume all 20 tokens")
    for i in range(20):
        limiter.check("customer", 0)
    print("  Bucket: 0 tokens")
    
    print("\nT=0ms: Next request denied")
    result = limiter.check("customer", 0)
    print(f"  DENIED - Retry after: {result.retry_after_ms}ms")
    
    print("\nT=2000ms: After 2 seconds, bucket refilled")
    print("  Refill: 0 + (2 * 5) = 10 tokens")
    result = limiter.check("customer", 2000)
    print(f"  Request: {'ALLOWED' if result.allowed else 'DENIED'} | Remaining: {result.remaining}")


def demo_capacity_cap():
    print_section("Demo 3: Capacity Cap")
    limiter = TokenBucketRateLimiter(capacity=50, refill_rate=10)
    
    print("\nScenario: Capacity 50, refill rate 10/sec")
    print("\nT=0ms: Consume all 50 tokens")
    for i in range(50):
        limiter.check("api-user", 0)
    print("  Bucket: 0 tokens")
    
    print("\nT=20000ms: Wait 20 seconds (would be 200 tokens without cap)")
    print("  Refill calculation: 0 + (20 * 10) = 200")
    print("  With cap: min(200, 50) = 50 tokens")
    result = limiter.check("api-user", 20000)
    print(f"  Bucket capped at: {result.remaining + 1} tokens")


def demo_multiple_users():
    print_section("Demo 4: Multiple Independent Users")
    limiter = TokenBucketRateLimiter(capacity=5, refill_rate=1)
    
    print("\nScenario: 5 capacity, 1 token/sec, two users")
    
    print("\nUser A makes 4 requests at T=0ms:")
    for i in range(4):
        result = limiter.check("user-a", 0)
        print(f"  Request {i+1}: ALLOWED | Remaining: {result.remaining}")
    
    print("\nUser B makes 3 requests at T=0ms:")
    for i in range(3):
        result = limiter.check("user-b", 0)
        print(f"  Request {i+1}: ALLOWED | Remaining: {result.remaining}")
    
    print("\nUser A tries 2 more at T=0ms:")
    for i in range(2):
        result = limiter.check("user-a", 0)
        status = "ALLOWED" if result.allowed else "DENIED"
        print(f"  Request {5+i}: {status:7} | Remaining: {result.remaining}")
    
    print("\nUser B tries 3 more at T=0ms:")
    for i in range(3):
        result = limiter.check("user-b", 0)
        status = "ALLOWED" if result.allowed else "DENIED"
        print(f"  Request {4+i}: {status:7} | Remaining: {result.remaining}")
    
    print("\nNotice: Each user has independent quota")


def demo_spec_scenario():
    print_section("Demo 5: Full Spec Scenario")
    limiter = TokenBucketRateLimiter(capacity=100, refill_rate=10)
    
    print("\nCustomer: stripe-test")
    print("\nT=0ms: 60 requests arrive")
    allowed = sum(1 for _ in range(60) if limiter.check("stripe-test", 0).allowed)
    print(f"  Served: {allowed} | Remaining in bucket: 40")
    
    print("\nT=2000ms: Refill (40 + 2*10 = 60), then 70 requests")
    allowed = denied = 0
    for _ in range(70):
        result = limiter.check("stripe-test", 2000)
        if result.allowed:
            allowed += 1
        else:
            denied += 1
    print(f"  Served: {allowed} | Denied: {denied} | Remaining: 0")
    
    print("\nT=7000ms: Refill (0 + 5*10 = 50), then 30 requests")
    allowed = sum(1 for _ in range(30) if limiter.check("stripe-test", 7000).allowed)
    print(f"  Served: {allowed} | Remaining: 20")
    
    print("\nT=17000ms: Refill (20 + 10*10 = 120 -> cap 100), then 80 requests")
    allowed = sum(1 for _ in range(80) if limiter.check("stripe-test", 17000).allowed)
    print(f"  Served: {allowed} | Remaining: 20")


if __name__ == "__main__":
    demo_basic()
    demo_refill()
    demo_capacity_cap()
    demo_multiple_users()
    demo_spec_scenario()
    
    print_section("All Demos Complete")
    print()
