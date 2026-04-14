Implementation Notes - Token Bucket Rate Limiter

ARCHITECTURE

On-demand continuous refill instead of background timer. When check() is called, elapsed time is calculated and tokens are added based on that elapsed time. This avoids threading complexity and naturally handles long idle periods.

DATA STRUCTURES

Two dictionaries per customer:
- buckets: Maps customer_id (str) to current token count (float)
- last_refill: Maps customer_id (str) to last refill timestamp (int milliseconds)

Float tokens preserve precision in fractional accumulation. Integer conversion only happens when returning remaining count to caller.

KEY DESIGN DECISIONS

1. Float tokens internally: Preserves fairness for small time intervals. 50ms at 10 tokens/sec earns 0.5 tokens, not 0.

2. On-demand refill: Calculate elapsed time per request, no background tasks. Scales better and more testable.

3. Capacity capping: Applied after refill to prevent overflow during long idle periods.

4. Per-customer isolation: Each customer in separate dict entries with zero cross-contamination.

TESTING STRATEGY

10 test cases across 8 test classes organized by concern:

Scenario tests (test_scenario.py):
- Initialization: First request gets full capacity
- Basic rate limiting: Allow/deny enforcement
- Refill mechanism: Token accumulation over time
- Multiple customers: Independent quotas
- Full spec scenario: End-to-end validation

Edge case tests (test_edge_cases.py):
- Capacity cap: Long idle doesn't overflow
- Retry timing: Millisecond conversion accuracy
- Fractional tokens: Precision with small intervals
- Empty bucket: Proper rejection handling

POTENTIAL EXTENSIONS

1. Thread safety: Add locks for concurrent access
2. Distributed: Use Redis/Memcached for multiple servers
3. Monitoring: Track rejection rate, average tokens used
4. User tiers: Different rate limits for different user types
5. Cleanup: Remove inactive customers after timeout to save memory
6. Metrics: Per-customer usage statistics and rate patterns


