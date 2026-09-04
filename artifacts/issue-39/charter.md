# charter.md - this task's charter (turn 0, strong model): every item [assumed] until a probe confirms it; adds to the laws, never relaxes them
packs: writing, judging, code

## Interpretation
[assumed] The deliverable is 'script.json', a rigidly structured comedic script containing TTS metadata (pitch/rate), exact subtitles, and >=3 cutaway timestamps, totaling 60-115 seconds in length. The tone must be aggressive satire matching 'constitution.md' and achieving >=8.0 on a subjective rubric. Crucially, I must inspect 'manifest.md' from task 1 immediately; if it is a stub or degenerate, I must reject it via the Swarm Channel and abort.

## Strategy
[assumed] 1. Turn 1: Read 'manifest.md', 'constitution.md', and 'artifacts/issue-38/slice.html'. 2. Turn 2: Validate input. If 'manifest.md' is missing or dummy text, use the GitHub API to post 'INPUT-REJECT: #<issue>' and declare impossible. 3. Turn 3-4: Write criteria.md and verify.py. Mechanical checks: JSON parser, required keys, gag count >= 3, duration heuristic (words/2.5 + cutaways*3). Subjective check: gemini-3.1-pro-preview scoring >=8.0 against the constitution rubric. 4. Turn 5: Create directories and files for 5 degenerate twins. 5. Turn 6: Run verify.py RED against twins. 6. Turn 7: Prompt gemini-3.5-flash via metered.generate to produce a V1 rough draft as a Python dictionary, dumped to 'script.json'. 7. Turn 8-20: Iterate based on verify.py subjective feedback, prompting the model to push boundaries until the satire score hits 8.0. 8. Turn 21: Output the final format-proving 'manifest.md' next to 'script.json'.

## Risks and cheap probes
[assumed] 1. Upstream failure: 'manifest.md' is a placeholder, trapping the agent in an invalid state. Probe: Read it on Turn 1 and aggressively abort if invalid. 2. Duration ambiguity: The prompt requests 60-115 seconds, but text has no inherent duration. Probe: Implement a strict programmatic word-count-to-seconds multiplier in verify.py. 3. Subjective bar failure: Satire is hard for standard models, risking an endless scoring loop. Probe: Pass the explicit 'edgy Family Guy and South Park style' directive and constitution.md directly into the gemini-3.5-flash generation prompt.

## Candidate twins (write them under twins/ on turn 1 or 2)
- twins/empty: Valid JSON object with an empty dialogue array (fails minimal content check).
- twins/short: Valid schema but only 50 words total (fails the 60-115 second duration check).
- twins/no_gags: Correct length and schema, but contains 0 cutaway timestamps (fails the >= 3 gag check).
- twins/bland: Correct length and schema, but text is polite, generic corporate dialogue (fails the subjective 8.0 satire threshold).
- twins/no_tts: Dialogue objects missing the required 'pitch' and 'rate' keys (fails schema mechanical check).

## Task rules (add to the laws; never relax them)
- [assumed] VALIDATE INPUT FIRST: On Turn 1, read 'manifest.md'. If it contains placeholders, lorem ipsum, or is missing structural data, construct the GitHub API call using GITHUB_TOKEN to post 'INPUT-REJECT: #<issue_num> <evidence>' to issue #39, then exit action='impossible'.
- [assumed] MECHANICAL TIMING: Compute duration in verify.py explicitly as '(total_words / 2.5) + (num_cutaways * 3)' to convert the text script into an objective, checkable 60-115 second window.
- [assumed] JSON SAFETY: Never write 'script.json' directly from string output. Prompt the generation model to return valid Python code containing a dictionary, execute it, and write the file using 'json.dump()' to guarantee parseability.
