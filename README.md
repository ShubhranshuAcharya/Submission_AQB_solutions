Token Bucket Rate Limiter

Candidate: Shubhranshu Acharya
Language: Python

⸻

Overview

This project implements a per-customer Token Bucket Rate Limiter, a widely used technique in distributed systems to control request rates and ensure fair resource usage.

The system enforces:
	•	Capacity: 100 tokens per customer
	•	Refill Rate: 10 tokens per second
	•	Cost per Request: 1 token

If a request cannot be served, the system returns a precise retry time in milliseconds.

⸻

Design Philosophy

Instead of using a background refill process, I implemented an on-demand refill strategy.

Why this approach?
	•	Eliminates the need for background threads
	•	Avoids synchronization complexity
	•	Naturally handles idle periods
	•	Scales efficiently with the number of users

This approach aligns closely with real-world production systems.

⸻

Core Approach

Each customer is tracked independently using:
	•	tokens → current available tokens (float for precision)
	•	last_refill → timestamp of last update

Flow per request:
	1.	Compute elapsed time since last request
	2.	Refill tokens proportionally
	3.	Cap tokens at maximum capacity
	4.	Allow or reject request:
	•	If allowed → consume 1 token
	•	If rejected → compute retry time

⸻

Precision Consideration

Tokens are stored as floating-point values to ensure fairness in high-frequency scenarios.

Example:
50 ms elapsed at 10 tokens/sec results in 0.5 tokens.

Without floating-point precision, such short intervals would incorrectly produce 0 tokens, leading to unfair throttling.

⸻

Issues Identified in Starter Code

The provided starter code had the following issues:

1. Incorrect Initialization

The bucket was initialized with 0 tokens instead of full capacity, causing the first request to fail.

2. Missing Capacity Cap

Tokens could exceed the maximum capacity after long idle periods, breaking rate limiting guarantees.

3. Incorrect Retry Time Units

Retry time was returned in seconds instead of milliseconds, leading to incorrect client behavior.

⸻

Scenario Walkthrough
	•	Initial burst requests are allowed until tokens are exhausted
	•	Tokens refill correctly over time
	•	Excess tokens are capped at capacity
	•	Rejected requests receive accurate retry timing

This confirms both correctness and realistic system behavior.

⸻

Project Structure
submission/
│
├── APPROACH.md              # Detailed explanation of design decisions
│
├── src/
│   ├── main.py              # Core rate limiter implementation
│   ├── types.py             # Data models (Decision class)
│   └── utils.py             # Helper utilities
│
├── tests/
│   ├── test_scenario.py     # Functional test cases
│   └── test_edge_cases.py   # Boundary and edge testing
│
├── demo/
│   └── simulate.py          # End-to-end simulation
│
├── IMPLEMENTATION_NOTES.md  # Trade-offs and reasoning
└── AI_USAGE_LOG.md          # Transparency log

Key Engineering Decisions
	•	On-demand refill over background jobs
	•	Floating-point token handling for fairness
	•	Strict capacity enforcement
	•	Deterministic retry time calculation

⸻

Complexity
	•	Time Complexity: O(1) per request
	•	Space Complexity: O(N) for N customers

⸻

Highlights
	•	Clean and minimal implementation (~55 LOC)
	•	No external dependencies
	•	Deterministic and testable design
	•	Handles edge cases (idle time, burst traffic, precision)

⸻

Final Thoughts

This solution focuses on building a production-ready, scalable, and precise rate limiter.

The implementation avoids unnecessary complexity while ensuring correctness under all scenarios, making it suitable for real-world systems.
