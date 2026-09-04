# charter.md - this task's charter (turn 0, strong model): every item [assumed] until a probe confirms it; adds to the laws, never relaxes them
packs: code, writing

## Interpretation
[assumed] We must validate the technical feasibility of the 'crude SVG + Web Speech API' constraint. This requires explicitly documenting the lack of neural media generators in `capabilities.md`, creating a functional 10-second end-to-end tracer slice (`slice.html`) with a 9:16 aspect ratio, one inline SVG character, and one speech API call, plus a `manifest.md` detailing the file formats and SVG IDs.

## Strategy
[assumed] 1. Write `capabilities.md` immediately, explicitly noting the absence of neural media generators. 2. Write `criteria.md` outlining the requirements for the three deliverables (`capabilities.md`, `slice.html`, `manifest.md`). 3. Write `verify.py` using `verify_kit.py` to check for specific strings (e.g., `<svg>`, `speechSynthesis`, `9/16`). Run it RED. 4. Build `slice.html`, implementing a 'Click to Play' button to bypass browser autoplay restrictions, rendering one SVG character, and sequencing one line of speech. 5. Write `manifest.md` mapping out the SVG structure and animation methodology. 6. Refine until `verify.py` passes the real artifact and fails all twins.

## Risks and cheap probes
[assumed] 1. Browser autoplay policies block `window.speechSynthesis` without user interaction. Probe: Require a 'Start' or 'Play' button in `slice.html`'s DOM. 2. Animation timing drifts from speech. Probe: Verify `slice.html` uses `SpeechSynthesisUtterance` events (`onend`, `onstart`) to trigger the animation cut rather than blind timeouts. 3. Failing the strict vertical format constraint. Probe: Assert the presence of `aspect-ratio: 9/16` or `1080`x`1920` sizing in the CSS via `verify.py`.

## Candidate twins (write them under twins/ on turn 1 or 2)
- twins/missing_capabilities: A directory where `capabilities.md` does not exist.
- twins/no_speech_api: A `slice.html` that uses `<audio>` or text but lacks `window.speechSynthesis`.
- twins/horizontal_video: A `slice.html` where the main container CSS is set to `aspect-ratio: 16/9` instead of 9/16.
- twins/raster_graphics: A `slice.html` that uses an `<img>` tag instead of inline `<svg>` elements.
- twins/empty_manifest: A `manifest.md` that fails to document specific SVG IDs and the JSON/Markdown data passing structure.

## Task rules (add to the laws; never relax them)
- [assumed] 1. `slice.html` MUST include a user-interaction trigger (e.g., `<button id="start">`) to initiate the Web Speech API; it cannot attempt to autoplay audio on load.
- [assumed] 2. All character visuals in `slice.html` must be strictly inline `<svg>` tags using basic geometric elements (`<rect>`, `<circle>`, `<path>`). Absolutely no `<img>`, `<video>`, or external media links are permitted.
- [assumed] 3. `capabilities.md` must be written first and explicitly declare that image generation, text-to-video, and text-to-speech are missing or unreachable.
