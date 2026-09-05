# charter.md - this task's charter (turn 0, strong model): every item [assumed] until a probe confirms it; adds to the laws, never relaxes them
packs: code, perception, writing

## Interpretation
[assumed] The 'Tracer Slice' is a proof-of-concept proving all moving parts (CSS animations, SVG rendering, Web Speech API, interaction requirements) can function perfectly in a single zero-dependency HTML file. 'Massive Tap to Play overlay' means a full-viewport, high z-index DOM element that blocks all other content and captures the first user interaction to unlock browser autoplay policies. 'Mouth flapping synced' means JavaScript toggles a CSS animation class on an SVG `<g>` element based on the `speechSynthesis` `onstart` and `onend` events. 'One cut' means JavaScript swapping visibility of two distinct scene containers after a set timeout.

## Coverage table (one row = one claim in criteria.md = one typed check in verify.py; file | field or constraint | requirement | check)
- capabilities.md | content | file exists and contains tool probe results | os.path.exists() and len(read_file) > 0
- slice.html | validity | file exists and decodes as valid HTML | html.parser.HTMLParser() parsing without errors
- slice.html | dependencies | zero external resources | regex/AST check ensuring no <script src=>, <link href=>, or external <img src=>
- slice.html | autoplay gating | speech API triggers only on interaction | headless browser test asserting no speech logs before click, and speech logs after click
- slice.html | aspect ratio | strict 9:16 visual ratio | headless browser layout extraction or CSS substring parse for 'aspect-ratio: 9/16' or equivalent math
- slice.html | visual rendering | rendering confirms 'Tap to Play' overlay, SVG character, and 1 cut | kit.perceive() on a screenshot captured via headless browser
- slice.html | animation sync | JS class toggles sync with speech | JS AST inspection or headless DOM log verification of mouth class addition matching speech timing
- manifest.md | contract validity | contains exact runtime, start overlay boolean, and JSON speech settings | json.loads() applied to a markdown JSON block, verifying schema keys
- slice.html | alignment | strictly obeys constitution.md | kit.judge() reading constitution.md against slice.html raw text
- slice.html | subjective quality | 8.0/10 on Technical Execution rubric | kit.judge() on headless screenshots + captured interaction logs

## Strategy
[assumed] Turn 1: Probe the environment to see if Playwright or Selenium is installed; if not, use a `subprocess` to `pip install playwright && playwright install chromium` to enable headless browser tests, recording this to `capabilities.md`. Turn 2: Write `criteria.md` establishing the mechanical and subjective claims. Turn 3: Build `verify.py` using `verify_kit`, ensuring the visual/audio verification uses a Python script to serve `slice.html`, click the overlay via Playwright, capture a screenshot, and intercept `console.log` messages for Web Speech API triggers, feeding the artifacts to `kit.perceive`. Turn 4: Create five degenerate twins simulating common failures (autoplay violation, broken speech, static SVG). Turn 5-8: Write `manifest.md` and build `slice.html` natively, refining the inline CSS, SVG, and JS based on `verify.py` outputs until it passes.

## Risks and cheap probes
[assumed] 1. Headless Browser Unavailability: `verify.py` cannot capture visual state natively. PROBE: Write a fast Python script to import/install Playwright and snap a picture of a dummy HTML file. 2. Web Speech API limitations in headless mode: `speechSynthesis` might not generate actual audio or trigger events reliably in headless Chromium. PROBE: Inject `console.log` inside the `speechSynthesis.onboundary`/`onend` events and capture them via the headless browser's page-log listener. 3. Aspect Ratio Failure: `9:16` might not render correctly on desktop model viewports. PROBE: Force the Playwright viewport to a mobile resolution (e.g., 375x667) before capturing.

## Candidate twins (write them under twins/ on turn 1 or 2)
- twins/autoplay_violation: slice.html calls `speechSynthesis.speak()` directly on load without requiring an interaction overlay.
- twins/mute_character: slice.html has the overlay and animation but never invokes the Web Speech API.
- twins/static_mouth: slice.html plays audio but the SVG character lacks any CSS animation or JS class toggling for the mouth.
- twins/desktop_ratio: slice.html fails to enforce the 9:16 aspect ratio (no aspect-ratio CSS or fixed mobile dimensions).
- twins/invalid_manifest: manifest.md is missing the required JSON map of speech settings or boolean start confirmation.
- twins/stub_content: slice.html uses placeholder text like 'TODO' or 'SVG GOES HERE' instead of an actual crude character.

## Task rules (add to the laws; never relax them)
- [assumed] ZERO EXTERNAL DEPENDENCIES: `slice.html` must contain 100% of its CSS, JS, and SVG inline. Do not link to any external fonts, scripts, or media.
- [assumed] AUTOPLAY GATING: The `window.speechSynthesis.speak()` method MUST NOT be called in the global scope. It must exist strictly within the event listener attached to the 'Tap to Play' overlay.
- [assumed] HEADLESS VALIDATION: To measure rendering and audio triggering, `verify.py` must use a Python-based headless browser to click the overlay, capture a DOM screenshot, capture console logs reporting speech events, and feed both to `kit.perceive` or `kit.judge`.
