<h1>Token Bucket Rate Limiter</h1>

<p><b>Candidate:</b> Shubhranshu Acharya<br>
<b>Language:</b> Python</p>

<hr>

<h2>Overview</h2>

<p>
This project implements a per-customer Token Bucket Rate Limiter, a widely used technique in distributed systems to control request rates and ensure fair resource usage.
</p>

<p>The system enforces:</p>
<ul>
<li>Capacity: 100 tokens per customer</li>
<li>Refill Rate: 10 tokens per second</li>
<li>Cost per Request: 1 token</li>
</ul>

<p>If a request cannot be served, the system returns a precise retry time in milliseconds.</p>

<hr>

<h2>Design Philosophy</h2>

<p>
Instead of using a background refill process, I implemented an on-demand refill strategy.
</p>

<p><b>Why this approach?</b></p>
<ul>
<li>Eliminates the need for background threads</li>
<li>Avoids synchronization complexity</li>
<li>Naturally handles idle periods</li>
<li>Scales efficiently with the number of users</li>
</ul>

<p>This approach aligns closely with real-world production systems.</p>

<hr>

<h2>Core Approach</h2>

<p>Each customer is tracked independently using:</p>
<ul>
<li>tokens → current available tokens (float for precision)</li>
<li>last_refill → timestamp of last update</li>
</ul>

<p><b>Flow per request:</b></p>
<ol>
<li>Compute elapsed time since last request</li>
<li>Refill tokens proportionally</li>
<li>Cap tokens at maximum capacity</li>
<li>Allow or reject request:
  <ul>
    <li>If allowed → consume 1 token</li>
    <li>If rejected → compute retry time</li>
  </ul>
</li>
</ol>

<hr>

<h2>Precision Consideration</h2>

<p>
Tokens are stored as floating-point values to ensure fairness in high-frequency scenarios.
</p>

<p>
Example: 50 ms elapsed at 10 tokens/sec results in 0.5 tokens.
</p>

<p>
Without floating-point precision, such short intervals would incorrectly produce 0 tokens, leading to unfair throttling.
</p>

<hr>

<h2>Issues Identified in Starter Code</h2>

<p><b>1. Incorrect Initialization</b><br>
The bucket was initialized with 0 tokens instead of full capacity, causing the first request to fail.</p>

<p><b>2. Missing Capacity Cap</b><br>
Tokens could exceed the maximum capacity after long idle periods, breaking rate limiting guarantees.</p>

<p><b>3. Incorrect Retry Time Units</b><br>
Retry time was returned in seconds instead of milliseconds, leading to incorrect client behavior.</p>

<hr>

<h2>Scenario Walkthrough</h2>

<ul>
<li>Initial burst requests are allowed until tokens are exhausted</li>
<li>Tokens refill correctly over time</li>
<li>Excess tokens are capped at capacity</li>
<li>Rejected requests receive accurate retry timing</li>
</ul>

<p>This confirms both correctness and realistic system behavior.</p>

<hr>

<h2>Project Structure</h2>

<pre>
submission/
│
├── APPROACH.md
│
├── src/
│   ├── main.py
│   ├── types.py
│   └── utils.py
│
├── tests/
│   ├── test_scenario.py
│   └── test_edge_cases.py
│
├── demo/
│   └── simulate.py
│
├── IMPLEMENTATION_NOTES.md
└── AI_USAGE_LOG.md
</pre>

<hr>

<h2>Key Engineering Decisions</h2>

<ul>
<li>On-demand refill over background jobs</li>
<li>Floating-point token handling for fairness</li>
<li>Strict capacity enforcement</li>
<li>Deterministic retry time calculation</li>
</ul>

<hr>

<h2>Complexity</h2>

<p>
Time Complexity: O(1) per request<br>
Space Complexity: O(N) for N customers
</p>

<hr>

<h2>Highlights</h2>

<ul>
<li>Clean and minimal implementation (~55 LOC)</li>
<li>No external dependencies</li>
<li>Deterministic and testable design</li>
<li>Handles edge cases (idle time, burst traffic, precision)</li>
</ul>

<hr>

<h2>Final Thoughts</h2>

<p>
This solution focuses on building a production-ready, scalable, and precise rate limiter.
</p>

<p>
The implementation avoids unnecessary complexity while ensuring correctness under all scenarios, making it suitable for real-world systems.
</p>