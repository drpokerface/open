# charter.md - this task's charter (turn 0, strong model): every item [assumed] until a probe confirms it; adds to the laws, never relaxes them
packs: writing, judging, code

## Interpretation
[assumed] The primary task is to write a comedy short script (60-119s) with an absurd, fast-paced, original IP cutaway style, delivered as `script.json` and `manifest.md`. The script must include scenes, dialogue lines, Web Speech API character settings (pitch, rate), and millisecond timings. A strict prerequisite is validating `artifacts/issue-55/slice.html` against its manifest; if the input is a stub or broken, I must issue an INPUT-REJECT to the swarm channel and halt. A high subjective quality bar (>= 8/10) is judged against a constitution rubric.

## Coverage table (one row = one claim in criteria.md = one typed check in verify.py; file | field or constraint | requirement | check)
- script.json | parseable | Must be valid JSON | json.loads(kit.raw('script.json'))
- script.json | schema keys | Must contain scenes, dialogue, pitch, rate, offset_ms | python dictionary key checks on parsed json structure
- script.json | runtime | 60000 <= max(offset_ms) <= 119000 | python math calculating the bounds of offset_ms in the json arrays
- script.json | voice variation | pitch and rate must not be uniform | python set(pitch_values) and set(rate_values) length > 1
- script.json | original IP | 0 copyrighted names from major animation franchises | kit.judge('gemini-3.1-pro-preview', 'Contains 0 copyrighted characters/franchises (e.g. South Park, Family Guy)')
- script.json | subjective quality | Score >= 8/10 against Goal Constitution | kit.judge('gemini-3.1-pro-preview', 'quality >= 8', 'script.json', constitution_text, threshold=8)
- manifest.md | existence | File must exist alongside script.json | kit.exists('manifest.md')
- manifest.md | sample code | Must detail exact formats with a tiny sample | kit.has_all('manifest.md', ['```json', 'pitch', 'offset_ms'])

## Strategy
[assumed] 1. Turn 1: Read `artifacts/issue-55/slice.html`, the Task 1 manifest (if findable in artifacts/ or via search), and `artifacts/board-20260909-090123/constitution.md`. 2. Turn 2-3: Write a Python script to validate `slice.html`. If it lacks Web Speech logic or is a placeholder, use GitHub API to post `INPUT-REJECT: #55 <reason>` to issue #56 and execute `action: impossible`. 3. Turn 4: Write `criteria.md` and `verify.py` using `verify_kit`, plus degenerate twins (short runtime, copyright violation, unfunny). 4. Turn 5-6: Use `gemini-3.5-flash` to generate the initial script and manifest. 5. Turn 7+: Run `verify.py`. The verifier calculates total duration purely from the JSON's `offset_ms` + character count / speaking rate. The verifier uses `gemini-3.1-pro-preview` for the quality judge. Iterate the script based on judge feedback until it scores >= 8.

## Risks and cheap probes
[assumed] 1. Invalid or missing slice.html from Task 1. Probe: Read `artifacts/issue-55/slice.html` immediately and use regex to confirm the presence of Web Speech API calls (`SpeechSynthesisUtterance`). 2. Runtime calculation ambiguity. Probe: Strictly define runtime in `verify.py` as the maximum `offset_ms` plus a reasonable padding for the final line, enforcing the 60s-119s limit purely via python math on the parsed JSON. 3. Subjective bar failure. Probe: Seed the generation prompt heavily with the exact rubric from `constitution.md` and instruct the model to lean into extreme, non-copyrighted absurdity.

## Candidate twins (write them under twins/ on turn 1 or 2)
- twins/short_duration: Valid JSON format but the calculated offset_ms bounds fall under 60 seconds (fails runtime check).
- twins/copyright_ip: Script includes names like 'Cartman', 'Griffin', or 'Homer' (fails the 0 copyrighted names judge check).
- twins/flat_speech: Script lacks pitch or rate fields for characters, or they are all uniform (fails Web Speech API limitations parse check).
- twins/unfunny_generic: Script is a boring conversation about the weather (fails the subjective >= 8/10 constitution check).
- twins/missing_manifest: script.json is perfect but manifest.md is missing (fails file existence check).

## Task rules (add to the laws; never relax them)
- [assumed] You must validate slice.html first. If it is a stub, placeholder, or lacks Web Speech API implementations, you must post an 'INPUT-REJECT: #55' comment via the GitHub API to issue #56, then use action: impossible.
- [assumed] Runtime must be mechanically calculated in verify.py by summing or bounding the millisecond offsets in the JSON, not via LLM estimation.
- [assumed] The qualitative comedic check must use 'gemini-3.1-pro-preview' and the exact text of constitution.md.
