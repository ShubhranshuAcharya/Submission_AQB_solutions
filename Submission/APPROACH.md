Token Bucket Rate Limiter - Approach (hand-written)

Candidate: Shubhranshu Acharya    
Language: Python

Problem Understanding:

The task was to build a token bucket rate limiter. Each customer gets 100 tokens, each request consumes 1 token, and tokens refill at 10 per second. If no tokens are available, the request should be rejected and the wait time should be returned in milliseconds.

One confusing part was how the refill works. The description mentioned a background timer, but the example clearly followed an on-demand calculation. I decided to go with the on-demand approach since it's simpler and avoids threading.


Assumptions:

- Refill is calculated on-demand during each request, not using a background timer  
- Bucket starts full (100 tokens)  
- Tokens never go beyond capacity, even after long idle time  
- Each customer has an independent bucket  
- Wait time is returned in milliseconds  


Errors in Problem Statement:

I didn't find any major issues. The requirements were mostly clear.  
Only confusion was around background timer vs on-demand refill, but the example made it clear that on-demand was expected.


Bugs in Starter Code:

Bug 1:

The bucket was initialized with 0 tokens. Because of this, even the first request was getting rejected.

Fix: Initialize bucket with full capacity  
self.buckets[customer_id] = self.capacity

Bug 2:

There was no cap after refill. So after a long idle time, tokens could go above 100 (e.g., 200 tokens after 20 seconds), which breaks the rate limit.

Fix: Cap tokens using min() so they never exceed capacity

Bug 3:

Retry time was being returned in seconds instead of milliseconds.  
Because of integer conversion, small waits like 0.1 seconds became 0.

Fix: Multiply by 1000 to convert to milliseconds before returning

Solution Design:

I used two dictionaries:
- One to store current tokens (float)
- One to store last refill timestamp

On each request:
- Calculate time passed since last request  
- Add tokens based on time  
- Cap tokens at capacity  
- If tokens >= 1 → allow and deduct 1  
- Else → reject and calculate wait time  

I used float tokens so that small time intervals are handled correctly.  
For example, 50ms at 10 tokens/sec gives 0.5 tokens instead of 0.

I preferred on-demand refill because:
- No threads needed  
- Simpler logic  
- Works naturally for long idle times  
- Easier to test  

The implementation is around 55 lines, uses simple data structures, and no external dependencies.


Walkthrough of Example:

T = 0ms  
First request > allowed > 99 tokens left  

Next 59 requests > all allowed > 40 tokens left  

T = 2000ms  
2 seconds passed > refill = 40 + 20 = 60  
Request allowed > 59 tokens left  

Next 69 requests  
59 allowed > 10 rejected  

T = 7000ms  
5 seconds passed > refill = 50  
Request allowed  

Next 29 requests > all allowed > 20 tokens left  

T = 17000ms  
10 seconds passed > refill = 20 + 100 = 120 > capped at 100  
Request allowed  

Next 79 requests > all allowed > 20 tokens left  

All calculations match expected behavior.
