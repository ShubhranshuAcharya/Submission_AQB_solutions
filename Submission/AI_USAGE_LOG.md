# AI Interaction 1
Time: Start of project

Tool: AI Assistant (ChatGPT / Claude)

My Prompt: Can you explain how the token bucket algorithm works for rate limiting, especially the difference between a background timer approach and a continuous on-demand refill approach?
What I Kept: The conceptual understanding that calculating elapsed time dynamically on each request is simpler, avoids threading, and scales better than maintaining active background timers.

What I Changed/Rejected: I didn't copy any generated code. I structured my own two-dictionary architecture (`buckets` and `last_refill`) based purely on the explanation.

# AI Interaction 2
Time: Middle of project / debugging starter code

Tool: AI Assistant (ChatGPT / Claude)

My Prompt: I have some starter code for a Token Bucket rate limiter. Can you help point out any bugs relating to capacity limits, initialization, and retry timings?

What I Kept: The AI's identification of three critical edge cases: the bucket initializing at 0 instead of max capacity, the lack of a capacity cap after long idle times, and the retry time computing in seconds rather than milliseconds.

What I Changed/Rejected: I rejected the AI's suggested code rewrites and wrote the actual bug fixes myself inline. I also manually created my own 8 test classes to verify the fixes independently.

# AI Interaction 3
Time: End of project / Final Testing

Tool: AI Assistant (Gemini/ antigravity)

My Prompt: "solve" along with a terminal output showing `pytest` failing with `ImportError: cannot import name 'Decision' from 'types' (C:\...\Python312\Lib\types.py)`.

What I Kept: The realization that my local `types.py` file was colliding with Python's built-in standard library `types` module. We renamed it to `models.py` and updated the imports in `main.py` to fix the test suite. 

What I Changed/Rejected: Kept the exact file rename and import path updates as suggested, which allowed all 10 tests to successfully compile and pass.
