# providers.md - the swarm's tool CATALOG: what agents may use, how to call it, what it costs.
# A row is USABLE only when its "key env var" exists in the environment. Keys live in .env
# on each worker machine, NEVER in this repo. Agents probe a row with one tiny call before
# relying on it, and route every call through metered.py so the cost lands in spend.jsonl.
#
# To add a provider: subscribe yourself, put the key in .env on every worker machine,
# restart the workers, then add a row here and push - workers see it on their next pull.
# Agents may request one via a PROPOSE-PROVIDER comment; only you can subscribe.

| capability | provider / how to call | key env var | unit cost (₹ - EDIT to your billing) | notes |
|---|---|---|---|---|
| text, judging, structured JSON | google-genai: metered.generate("gemini-3.5-flash", ...) | GEMINI_API_KEY | ~₹8/M in, ~₹33/M out | default for routine calls |
| hard planning / judging | metered.generate("gemini-3.1-pro-preview", ...) | GEMINI_API_KEY | ~₹105/M in, ~₹840/M out | escalation only, on proven need. NOTE: gemini-3.5-pro is NOT on this key (404) - do not use it; gemini-3.1-pro-preview is the verified strong model. |
| video/audio assembly, resize, mux | ffmpeg (local CLI) | (none - free) | ₹0 | probe with `ffmpeg -version`; install if missing |
| image generation | (add yours) | | | |
| text-to-speech | (add yours) | | | |
| text-to-video | (add yours) | | | |
