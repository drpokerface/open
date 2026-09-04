# charter.md - this task's charter (turn 0, strong model): every item [assumed] until a probe confirms it; adds to the laws, never relaxes them
packs: code, judging, writing

## Interpretation
[assumed] The deliverable is a single, zero-dependency file `slice.html` embedding SVG, CSS, and JS. 'Relentless pacing' means animations and speech must be tightly sequenced in the JS event loop. Since headless JS execution with TTS is unreliable in isolated environments, `verify.py` must validate the execution logic using static analysis—passing the source code of `slice.html` to `gemini-3.5-flash` to confirm API calls (e.g., `window.speechSynthesis`) and timing logic, while `gemini-3.1-pro-preview` evaluates the script's edgy content and subjective quality against `artifacts/board-20260904-202814/constitution.md`.

## Strategy
[assumed] 1. Probe native browser APIs constraints (SpeechSynthesis boundaries/timeouts) and draft `capabilities.md`. 2. Create `criteria.md`, `twins/`, and a sealed `verify.py` using `verify_kit.py` and `gemini-3.5-flash` to statically read `slice.html` for CSS keyframes, SVG elements, and TTS JS. 3. Build a rough `slice.html` (~10s) with one geometric SVG character, a hardcoded TTS call, and a CSS cutaway transition. 4. Draft `manifest.md` detailing this architecture. 5. Iterate in judged loops, using `gemini-3.1-pro-preview` to score the HTML's dialogue, subtitle logic, and layout against the constitution, refining the JS to sync subtitles tightly.

## Risks and cheap probes
[assumed] 1. TTS API unreliability: Probe by writing a quick python script to verify that `gemini-3.5-flash` can accurately identify JS `SpeechSynthesisUtterance.onboundary` event listeners in a code string. 2. Verifier cannot run JS natively: Probe by passing a mock HTML string to the model to ensure it can successfully extract and validate DOM structure and JS execution flow. 3. Content filter blocking 'edgy' scripts: Probe by generating a mild 'satirical cutaway' script snippet via `gemini-3.5-flash` before embedding it in the final file.

## Candidate twins (write them under twins/ on turn 1 or 2)
- twins/missing_tts/slice.html: HTML with CSS animations but completely missing `window.speechSynthesis` API calls.
- twins/no_animation/slice.html: HTML with functional TTS but static SVG and no CSS keyframes.
- twins/no_sync/slice.html: HTML where subtitles are hardcoded statically and do not update via JS during the scene.
- twins/wrong_aspect/slice.html: HTML missing the 9:16 viewport CSS constraints (e.g., standard desktop layout instead).
- twins/bland_content/slice.html: Structurally perfect HTML but with generic, polite placeholder dialogue that fails the 'edgy satirical' rubric threshold.

## Task rules (add to the laws; never relax them)
- [assumed] Validation of `slice.html` mechanics MUST rely on static source code analysis via `gemini-3.5-flash` (reading the JS/DOM structure), not headless browser execution.
- [assumed] The `slice.html` file must be 100% self-contained: all SVG, CSS (forcing a 9:16 aspect ratio), and JS logic must be inline with zero external network requests.
- [assumed] Subtitle synchronization must be explicitly visible in the JavaScript logic (e.g., via `setTimeout` arrays or TTS boundary events).
