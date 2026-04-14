Token Bucket Rate Limiter - Approach (hand-written)

Candidate: Shubhranshu Acharya  
Language: Python

1. Problem Understanding:

My goal was to build a token bucket rate limiter. Each customer gets 100 tokens, uses 1 token per request, and tokens refill at 10 per second. When out of tokens, I needed to make sure it rejects the request and returns the required wait time in milliseconds.
While reading the requirements, I noticed a slightly confusing part about how the refill works. The description mentioned a background timer every second, but the example showed an on-demand calculation. I chose to implement the on-demand approach because it is simpler, requires no threading, and is far more scalable.

2. Assumptions:

To build this cleanly, I made the following assumptions:
1. Refill happens continuously on-demand per request, not from a background timer.
2. The bucket starts with full capacity, not empty.
3. Tokens never exceed capacity even after long idle periods.
4. Each customer operates in complete isolation with no shared quota.
5. Wait time must be converted and returned in milliseconds, not seconds.

3. Errors Found in Problem Statement:

I reviewed the problem statement and found no critical errors. The description was mostly clear about requirements and the example scenario was accurate. The only minor confusion I spotted was the background timer versus on-demand logic, but the example output made it clear which approach was intended.

4. Bugs Found in Starter Code:

Bug 1:
- I found that on line 36, the starter code was initializing a brand new bucket to 0 tokens.
- Because of this, the very first valid request was always getting improperly rejected.
- To fix it, I changed the logic to initialize the bucket fully at maximum capacity by writing self.buckets[customer_id] = self.capacity.

Bug 2:
- I noticed on line 45 that there was absolutely no capacity cap applied after the continuous refill math occurred. 
- Left like that, a long idle period would generate something like 200 tokens for a 20-second wait, breaking the limit entirely.
- I fixed this by forcing a cap so the current tokens never mathematically exceed self.capacity. I did this using the min function.

Bug 3:
- I discovered on line 66 that the retry_after_ms variable was calculating the return value in standard seconds instead of milliseconds.
- A 0.1-second wait was just returning 0 due to the integer cast, meaning a client would retry immediately and fail.
- I fixed this by multiplying the mathematical remainder by 1000 so that it correctly scales into pure milliseconds before returning.

5. My Solution Design:

I designed a solution using exactly two dictionaries per customer: one to track their token count (as a floating point) and another to track their last refill timestamp. On each request, I calculate the elapsed time, mathematically add the proper refill tokens, cap it at capacity, and then either consume 1 token if allowed or calculate the remaining wait time if denied.
I deliberately chose to use float tokens to preserve precision, so a 50ms wait at 10 tokens per second earns 0.5 tokens instead of 0. This guarantees fairness.
I chose on-demand over a background timer because it completely eliminates threads, complex timing issues, and makes the system much easier for me to test.
My final code is 55 clean lines, uses two dicts, one dataclass, strict type hints, and has zero external dependencies.

6. Walkthrough of Example Scenario: 

I manually verified that my code handles the scenario flawlessly:

T=0ms: First request from customer. Bucket has 100 tokens. Request allowed. 99 remaining.
T=0ms: 59 more requests. All allowed consuming 59 tokens. 40 remaining.
T=2000ms: 2 seconds elapsed. Refill 40 + (2 x 10) = 60 tokens. Request allowed. 59 remaining.
T=2000ms: 69 more requests arrive. 59 allowed, 10 denied (bucket exhausted).
T=7000ms: 5 seconds elapsed. Refill 0 + (5 x 10) = 50 tokens. Request allowed.
T=7000ms: 29 more requests all allowed consuming tokens. 20 remaining.
T=17000ms: 10 seconds elapsed. Refill 20 + (10 x 10) = 120 but I cap it at 100. Request allowed.
T=17000ms: 79 more requests all allowed. 20 remaining.

Every calculation I tested matches the spec exactly.
