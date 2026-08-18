# benchmark/ - the self-hosting benchmark's goal set

One goal per `.txt` file. `python swarm.py benchmark` (with `ENABLE_BENCHMARK=1` in
`.env`) runs each goal through a fresh seed process and scores how many reach DONE.
`swarm.py amend` uses the same score to measure a proposed philosophy amendment:
system with vs. system without.

Rules of a good benchmark goal:
- SMALL: passable within BENCH_MAX_TURNS (default 25) and BENCH_TOKEN_BUDGET (default 300k).
- GENERAL: exercises a different skill per goal (data, tooling, web, text...), never
  one specific past failure - amendments must be measured on held-out work.
- CHECKABLE: a concrete deliverable that verify.py can measure mechanically.

Every benchmark run spends real API tokens (one capped seed run per goal, times two
when amend compares with/without). Edit or replace these goals freely.
