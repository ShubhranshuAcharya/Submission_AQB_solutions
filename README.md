Token Bucket Rate Limiter - Approach (hand-written)

Candidate: Shubhranshu Acharya  
Language: Python

PROBLEM UNDERSTANDING:

Build a token bucket rate limiter. Each customer gets 100 tokens, uses 1 per request, tokens refill at 10 per second. When out of tokens reject and return wait time in milliseconds.

The confusing part was how refill works. Problem description mentioned a background timer every second but the example showed on-demand calculation. I chose on-demand - simpler, no threading, more scalable.

ASSUMPTIONS:

1. Refill happens on-demand per request not from a background timer.
2. Bucket starts with full capacity not empty.
3. Tokens never exceed capacity even after long idle periods.
4. Each customer is completely isolated no shared quota.
5. Wait time must be in milliseconds not seconds.

ERRORS FOUND IN PROBLEM STATEMENT:

No critical errors in problem statement. The description was mostly clear about requirements and the example scenario was accurate. Minor confusion was background timer vs on-demand but example made it clear which approach was intended.

BUGS FOUND IN STARTER CODE:

Bug 1: Line initializes bucket to 0. Should be self.capacity. First request always rejected.

Bug 2: No capacity cap after refill. Long idle gives 200 tokens for 20 second wait instead of capped 100. Rate limiting breaks.

Bug 3: retry_after_ms returns seconds not milliseconds. 0.1 second wait returns 0 instead of 100ms. Client retries immediately.

MY SOLUTION DESIGN :

Two dictionaries per customer track token count (as float) and last refill timestamp. On each request calculate elapsed time, add refill tokens, cap at capacity, consume 1 if allowed or calculate wait time if denied.

Float tokens preserve precision so 50ms at 10 tokens per second earns 0.5 tokens not 0. Fairness is maintained.

On-demand is better than background timer because no threads, no complex timing, long waits work naturally, easier to test.

Code: 55 lines, two dicts, one dataclass, type hints. No dependencies beyond dataclasses.

WALKTHROUGH OF EXAMPLE SCENARIO :

T=0ms: First request from customer. Bucket has 100 tokens. Request allowed. 99 remaining.

T=0ms: 59 more requests. All allowed consuming 59 tokens. 40 remaining.

T=2000ms: 2 seconds elapsed. Refill 40 + (2 * 10) = 60 tokens. Request allowed. 59 remaining.

T=2000ms: 69 more requests arrive. 59 allowed, 10 denied (bucket exhausted).

T=7000ms: 5 seconds elapsed. Refill 0 + (5 * 10) = 50 tokens. Request allowed.

T=7000ms: 29 more requests all allowed consuming tokens. 20 remaining.

T=17000ms: 10 seconds elapsed. Refill 20 + (10 * 10) = 120 but cap at 100. Request allowed.

T=17000ms: 79 more requests all allowed. 20 remaining.

Every calculation matches the spec exactly.
