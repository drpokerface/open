# charter.md - this task's charter (turn 0, strong model): every item [assumed] until a probe confirms it; adds to the laws, never relaxes them
packs: code, judging, writing

## Interpretation
[assumed] The task requires building a tracer slice for a purely code-driven video project. Because text-to-video and TTS APIs are unavailable, the slice must be a 10-second standalone HTML file (slice.html) using inline SVG for visuals, CSS for a strict 9:16 mobile container, and the browser native window.speechSynthesis for narration. A capability probe must be recorded in capabilities.md based on attested limits, and a manifest.md must explicitly map the assets, timelines, and voice profiles for the slice.

## Coverage table (one row = one claim in criteria.md = one typed check in verify.py; file | field or constraint | requirement | check)
- capabilities.md | Tool Probe | Must explicitly note the absence of text-to-video and text-to-speech tools | kit.has_all reading the file text to find mentions of capabilities.
- manifest.md | Headers | Must contain Asset Manifestation, Timeline Cues, and Voice Profiles | kit.has_all reading the markdown structure.
- manifest.md | Voice Profiles | Pitch must be 0.0-2.0 and rate 0.1-10.0 | Parse the markdown text to ensure floats are within the bounded ranges.
- slice.html | Interactive Start | Must contain a Play button to bypass autoplay blocks | Parse HTML DOM for a button element.
- slice.html | Container constraints | CSS must enforce aspect-ratio 9/16, max-width 1080px, max-height 1920px | Parse the HTML style block looking for these exact CSS properties.
- slice.html | Media Independence | Zero external media files allowed | Parse HTML DOM to assert zero occurrences of img src, audio src, and video tags.
- slice.html | Subtitles | Kinetic typography overlay container | Parse HTML DOM for a text overlay div element designed for subtitles.
- slice.html | Narration | Uses SpeechSynthesis API | Parse JS block in HTML to ensure window.speechSynthesis is called.
- slice.html | Comedic Cutaway Impact | Execution and timing must score 8.0 or higher | kit.judge calling gemini-3.5-flash with the script contents and manifest timeline to evaluate pacing and structure.

## Strategy
[assumed] First, create capabilities.md noting the lack of generative media tools. Second, draft manifest.md detailing the Asset Manifestation, Timeline Cues, and Voice Profiles for the 10-second tracer. Third, build slice.html featuring a mandatory Play button, a 9:16 CSS container (max 1080x1920), inline SVGs for one scene and one cutaway, and vanilla JS that sequences the SpeechSynthesis API. Fourth, write criteria.md and verify.py to parse the HTML/DOM for strict independence constraints (no external media) and use gemini-3.5-flash to judge comedy pacing against the manifest. Finally, run verify.py and iterate the slice until the gate passes.

## Risks and cheap probes
[assumed] Browser autoplay policies blocking TTS. Probe: Ensure slice.html uses an explicit Play button to initialize window.speechSynthesis. Syncing animation with voice. Probe: Drive visual DOM updates (the cutaway gag) using JavaScript timeouts tied to the speech utterance onstart/onend events rather than decoupled CSS. Evaluating subjective humor programmatically. Probe: Extract the timeline from manifest.md and feed it to kit.judge so the LLM understands the exact pacing of the visual and audio delivery without needing eyes.

## Candidate twins (write them under twins/ on turn 1 or 2)
- Twin 1: slice.html contains an HTML img tag pointing to an external URL instead of using inline SVG.
- Twin 2: slice.html CSS sets aspect-ratio to 16:9 instead of the mandatory 9:16 constraint.
- Twin 3: manifest.md lacks the Voice Profiles header or omits pitch and rate parameters.
- Twin 4: slice.html attempts to trigger window.speechSynthesis automatically on page load without a Play button.
- Twin 5: slice.html has no JavaScript code to toggle DOM elements for a visual cutaway gag.

## Task rules (add to the laws; never relax them)
- [assumed] All visual assets must be inline SVGs and narration must use window.speechSynthesis; zero external media files are permitted.
- [assumed] slice.html must require explicit user interaction (a Play button click) before starting any animation, DOM updates, or audio.
- [assumed] Deliver the tracer slice entirely within a single slice.html file using vanilla JS and CSS to guarantee standalone playback and ease of verification.
