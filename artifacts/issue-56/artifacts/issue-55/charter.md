# charter.md - this task's charter (turn 0, strong model): every item [assumed] until a probe confirms it; adds to the laws, never relaxes them
packs: code, perception, judging

## Interpretation
[assumed] The primary objective is to de-risk the Web Speech API timing constraint by building a 10s end-to-end tracer slice (slice.html) synchronized with a CSS/SVG cutout animation. We must first inventory capabilities into capabilities.md by parsing providers.md and environment variables for API keys. The verifier requires a headless browser to run the HTML, capture frames, and verify via model perception. No placeholders are allowed anywhere; the 10-second animation must be a fully functional, complete joke.

## Coverage table (one row = one claim in criteria.md = one typed check in verify.py; file | field or constraint | requirement | check)
- capabilities.md | existence | file existence | kit.exists('capabilities.md')
- manifest.md | existence and formats | file existence and markdown parsing | kit.exists('manifest.md') and kit.has_all('manifest.md', ['format', 'sample'])
- slice.html | existence | file existence | kit.exists('slice.html')
- slice.html | HTML validity | parses as valid HTML | bs4.BeautifulSoup(kit.raw('slice.html'), 'html.parser')
- slice.html | Speech API | presence of window.speechSynthesis | kit.has_all('slice.html', ['window.speechSynthesis'])
- slice.html | SVG and CSS | presence of svg and style tags | kit.has_all('slice.html', ['<svg', '<style'])
- slice.html | JS execution | runs without JS errors | headless browser console log listener asserting no error level logs
- slice.html | perceptual validation | frames depict cutout animation | kit.perceive('C_perception', 'frames depict cutout animation', captured_frames, 'Does this depict cutout animation?')
- slice.html | subjective quality | score >= 7/10 against Goal Constitution | kit.judge('C_quality', 'score >= 7', 'slice.html', constitution_text, captured_output_text, threshold=7)

## Strategy
[assumed] Turns 1-3: Read providers.md, check os.environ for keys, write capabilities.md. Read the constitution. Turns 4-6: Draft criteria.md and verify.py. Implement the headless capture using playwright or selenium. verify.py will extract frames and pass them to metered.generate with gemini-3.5-flash to verify cutout animation. Turns 7-9: Create twin directories and run verify.py RED. Turns 10-15: Build slice.html with a basic SVG character, CSS keyframes, and a window.speechSynthesis JS script that fires an event to start the animation precisely when the speech starts. Turns 16-20: Build manifest.md. Refine animation and timing until verify.py passes the subjective rubric > 7/10 using gemini-3.1-pro-preview.

## Risks and cheap probes
[assumed] 1. Web Speech API inconsistency: Browsers handle events inconsistently. Probe: Write a quick HTML script using onstart events and run via headless browser console logs to verify. 2. Headless Browser Audio Capture: Capturing Web Speech API audio in a headless browser might be difficult. Probe: Run a minimal headless script passing --autoplay-policy=no-user-gesture-required to verify audio and frame capture. 3. Model scoring inconsistency: Subjective rubric might fluctuate. Probe: Run a dummy generated SVG and text through kit.judge early to calibrate prompts.

## Candidate twins (write them under twins/ on turn 1 or 2)
- twins/blank: Empty HTML file to test rendering failure and zero-content checks.
- twins/no_speech: Valid SVG/CSS animation but lacks window.speechSynthesis calls to test API usage check.
- twins/no_svg: Uses speech API but uses standard DOM elements instead of SVG to test SVG presence check.
- twins/unsynced: Animation and speech are totally disjointed to fail subjective constitution scoring.
- twins/js_error: Contains a deliberate syntax error in the script tag to test JS error detection.
- twins/no_cutout: SVG present but does not look like cutout animation to the perception model.

## Task rules (add to the laws; never relax them)
- [assumed] Use playwright or selenium via pip inside the workspace for headless testing and frame extraction.
- [assumed] The synchronization in slice.html MUST be driven by Web Speech API events like utterance.onstart rather than hardcoded setTimeout delays.
- [assumed] Never generate stub text for slice.html; the punchline must be a complete, original, and valid comedic line.
