Implementation Notes - Token Bucket Rate Limiter

ARCHITECTURE:

I used an on-demand refill approach instead of a background timer.  
Each time check() is called, elapsed time is calculated and tokens are added based on that.

This keeps the design simple, avoids threading, and works well even after long idle periods.

DATA STRUCTURES:

Two dictionaries are used:

- buckets > stores current token count (float) for each customer  
- last_refill > stores last refill timestamp (in milliseconds)  

Tokens are stored as float to preserve precision. Conversion to integer only happens when returning values.

KEY DESIGN DECISIONS:

1. Float tokens :
Using float ensures small time intervals are handled correctly.  
Example: 50ms at 10 tokens/sec gives 0.5 tokens instead of 0.

2. On-demand refill :
Refill is calculated during each request instead of running a background process.  
This keeps the system simple and scalable.

3. Capacity cap :  
After refill, tokens are always capped at maximum capacity to prevent overflow.

4. Per-customer isolation :  
Each customer is handled independently with no shared state.

TESTING:

I tested both normal scenarios and edge cases:

- First request should succeed with full capacity  
- Correct allow/deny behavior under load  
- Tokens refill correctly over time  
- Multiple customers work independently  
- Tokens never exceed capacity  
- Retry time is returned correctly in milliseconds  
- Small time intervals (fractional tokens) behave correctly  
- Empty bucket rejects requests properly  

TRADE-OFFS:

- On-demand refill is simple, but tokens are only updated when a request comes in  
- In-memory storage is fast but not suitable for distributed systems without external storage  

POTENTIAL EXTENSIONS:

- Add thread safety for concurrent access  
- Use Redis for distributed rate limiting  
- Support different rate limits for different users  
- Add basic monitoring (usage and rejection rates)
