# code and tools - scale structure to the goal (pack: code)
- Structure is a tool, not a stage. A small task is worked directly by the node contract.
  A hard task builds capability as files: tools in tools/, worker scripts, standing
  prompts. A long task builds a standing program (agent.py) with its own loop and state
  files, run in CHUNKS - your code action starts it, it works, persists state to disk,
  and exits before the timeout; the next turn runs it again.
- Every tool obeys the node contract: its first line says what it is for and carries
  UNVALIDATED until it has caught an induced fault, then VALIDATED: <the fault caught>.
  Nothing trusts an UNVALIDATED tool; the FILE INDEX shows first lines only.
- verify.py runs on a STRANGER'S machine: pip-install its own imports at the top or stay
  stdlib, touch only relative paths, fail loudly when something is missing, ship the
  rubric and anchors inside the workspace. An environment crash on the verifier's machine
  is a verification failure YOU caused.
- Big files: write them with write_file, whole; read them with read_file and a precise
  question; never print a large file through code - that view is cut at 2000 chars in
  memory and you will misread a complete file as truncated.
- Environment: Python 3 with pip and network; GEMINI_API_KEY (and GITHUB_TOKEN when a
  swarm channel exists) are in os.environ for every subprocess; git works inside the
  workspace (git log, git diff, git checkout <sha> -- <file>).
