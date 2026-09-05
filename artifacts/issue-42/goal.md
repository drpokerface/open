Tracer Slice & Capability Probe

SHARED SPEC:
- Quality Bar: Crude, programmatic minimalism (geometric primitives). No hallucinated/complex visuals. Humor is sharp, relies on absurd escalation and frame-perfect timing (Reel Rule: 3s hook, 5s first laugh, 8-10s escalation).
- Conventions: 1080x1920 (9:16) portrait, 24 fps, MP4 format. 45-119 seconds long.
- Style: Flat bold colors, sans-serif bold text with strokes. Audio uses programmatic TTS with distinct pitch/speed variations.
- Integration: Strict adherence to programmatic compilation using local Python tools (e.g., moviepy, gTTS). NO cloud media APIs.
- You must strictly obey the GOAL CONSTITUTION (already provided via artifacts_needed) and name its rubric as your judging standard.

HARDEST FIRST: The riskiest assumption most likely to sink this goal is that a purely programmatic Python script can successfully generate and sync distinct local TTS voices with procedurally drawn shapes in a 1080x1920 24fps MP4, without relying on any external cloud media APIs. You will test this cheapest possible probe right now.

1. PROBE for the strongest reachable generation tools. Verify Python libraries available or installable (moviepy, gTTS, pyttsx3, Pillow). Record findings in `capabilities.md` - confirming no cloud APIs are used.
2. Build a TINY but COMPLETE end-to-end slice: a ~10-second 1080x1920 MP4 video containing one scene, one geometrically drawn character, one voiced line of TTS dialogue, and one cutaway. Assemble exactly the way the final task will assemble (via Python code).
3. Judge it against the exemplars. Its artifacts define the file naming, formats, quality floor, and assembly method for the whole board.
4. Package `capabilities.md`, your python tool script, the `slice.mp4`, and a `manifest.md` into ONE output file: `tracer_slice.zip`.

INTEGRATION CONTRACT: You must ship manifest.md inside tracer_slice.zip detailing exact filenames, formats, and a tiny sample proving the format.

JUDGING:
Mechanical facts: `tracer_slice.zip` exists, extracts successfully, contains all required files. MP4 decodes. Placeholder or stub content anywhere in the deliverable is an automatic FAIL.
Subjective/Perceptual: 0-10 score against the Goal Constitution's anchored rubric (Pass threshold: 7/10). verify.py must consume the deliverable exactly the way its audience will - decode and sample its ACTUAL content, failing degenerate output (blank, silent, empty, uniform, truncated) regardless of metadata. This includes one cheap model-perception call confirming the sampled video actually depicts a geometric character and contains audio dialogue.

Save the main deliverable as tracer_slice.zip.

Already provided in your working directory: artifacts/board-20260905-100213/constitution.md

SWARM CHANNEL: you are working issue #42 of the GitHub repo drpokerface/open (token in GITHUB_TOKEN env). If you discover work this plan is missing, you may post ONE comment on your own issue via the API starting exactly 'PROPOSE-TASK: ' (state: title, why, which existing deliverable it unblocks, what it produces). Facing an irreversible, genuinely ambiguous choice, you may post ONE comment starting exactly 'QUESTION: ', then continue on the reversible path without waiting. If a PROVIDED input artifact fails your validation (placeholder, degenerate, or broken contract), post ONE comment starting exactly 'INPUT-REJECT: #<producing issue number> ' plus one line of evidence - the swarm will reopen that task; then declare impossible honestly instead of building on garbage. If providers.md lacks an adequate tool for a capability this task needs, you may post ONE comment starting exactly 'PROPOSE-PROVIDER: ' (capability, best candidate service, pricing, what it unlocks) - the owner decides about subscribing; continue meanwhile on the best reachable tier. Never create issues yourself; an owner-side arbiter reviews and answers as an 'ARBITER re' comment on this issue.

LAST VERIFICATION FAILURE (repair this first):
VERIFY: FAIL by worker-1 (drpokerface)
its own RESULT reports the gate was not passed - sent back for retry, not closed.
gate: NOT passed (ran out of turns, budget, or rejections)
why: Stopping: reached the maximum number of turns.
