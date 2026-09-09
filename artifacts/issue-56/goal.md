Script and Timing Chords

Read manifest.md from Task 1. You must OPEN and VALIDATE slice.html against that manifest FIRST. If you find a rotten or placeholder input, you must INPUT-REJECT it through your swarm channel rather than build on it. Write the complete script for the under-2-minute comedy short. It must heavily channel the irreverent, absurd, and socially satirical tone of South Park or Family Guy (escalating absurdity, fast-paced, cutaway-heavy) using entirely original IP. Tailor the script for the Web Speech API limitations proven in the slice. Output script.json containing an array of scenes, dialogue lines, assigned character pitch/rate settings, and precise millisecond timing offsets for visual cues. Ship manifest.md next to your deliverable detailing exact formats and a tiny sample. You must obey the Goal Constitution provided in artifacts_needed. HOW THIS WILL BE JUDGED: Mechanical facts: script.json and manifest.md exist; JSON is valid; runtime calculated from timings is between 60s and 119s; zero copyrighted names used. Subjective quality: 0-10 score against the Goal Constitution rubric (sharp edge, comedic escalation, the hook), pass threshold 8/10. verify.py must consume the deliverable by decoding the JSON, checking all fields, and failing degenerate output (blank, silent, empty, uniform, truncated) regardless of metadata. Placeholder or stub content anywhere in the deliverable is an automatic FAIL at any threshold.

Save the main deliverable as script.json.

Already provided in your working directory: artifacts/board-20260909-090123/constitution.md, artifacts/issue-55/slice.html

SWARM CHANNEL: you are working issue #56 of the GitHub repo drpokerface/open (token in GITHUB_TOKEN env). If you discover work this plan is missing, you may post ONE comment on your own issue via the API starting exactly 'PROPOSE-TASK: ' (state: title, why, which existing deliverable it unblocks, what it produces). Facing an irreversible, genuinely ambiguous choice, you may post ONE comment starting exactly 'QUESTION: ', then continue on the reversible path without waiting. If a PROVIDED input artifact fails your validation (placeholder, degenerate, or broken contract), post ONE comment starting exactly 'INPUT-REJECT: #<producing issue number> ' plus one line of evidence - the swarm will reopen that task; then declare impossible honestly instead of building on garbage. If providers.md lacks an adequate tool for a capability this task needs, you may post ONE comment starting exactly 'PROPOSE-PROVIDER: ' (capability, best candidate service, pricing, what it unlocks) - the owner decides about subscribing; continue meanwhile on the best reachable tier. Never create issues yourself; an owner-side arbiter reviews and answers as an 'ARBITER re' comment on this issue.

LAST VERIFICATION FAILURE (repair this first):
VERIFY: FAIL by worker-1 (drpokerface)
its own RESULT reports the gate was not passed - sent back for retry, not closed.
gate: NOT passed (ran out of turns, budget, or rejections)
why: Stopping: the gate rejected the work 5 times.
last gate rejection: rejection 5/5:
verify.py must exist, exit 0, print FAULT-PROOF: <evidence>, and end with VERDICT: PASS. Its output was:
th a sharp edge and escalating absurdity, but the deliverable fails the technical execution constraint by providing a JSON script instead of the r
  C6 sample 2: 8.5 near 'comedy, sharp edge, escalating absurdity, original character' - The script delivers brilliant, highly cynical satire with exceptional comedic escalation and a perfect rapid-fire pace, though it is currently in JSON format rather than the final 
  C6 sample 3: 8.5 near 'comedy, sharp edge, escalating absurdity, original character' - Score: 8.5/10 - Passes threshold. Dimension 1 aligns with anchor 9 (exceptional comedy with a sharp edge), Dimension 2 aligns with anchor 7 (the JSON structure provides precise spe
C6: PASS - subjective comedy quality is >= 8 - measured: median 8.5 of [6.0, 8.5, 8.5] vs thr
