# Criteria

## Interpretation
- 'Tracer Slice' is a proof-of-concept proving all moving parts (CSS animations, SVG rendering, Web Speech API, interaction requirements) can function perfectly in a single zero-dependency HTML file.
- 'Massive Tap to Play overlay' means a full-viewport, high z-index DOM element that blocks all other content and captures the first user interaction to unlock browser autoplay policies.
- 'Mouth flapping synced' means JavaScript toggles a CSS animation class on an SVG `<g>` element based on the `speechSynthesis` `onstart` and `onend` events, or regular speech speaking state updates.
- 'One cut' means JavaScript swapping visibility of two distinct scene containers after a set timeout (e.g., at 5 seconds into a 10-second play).
- 'Zero external dependencies' means all CSS, JS, and SVG are embedded inline, with no remote HTTP/HTTPS links.

## Claims
- C1: capabilities.md content exists and contains tool probe results.
- C2: slice.html exists and decodes as valid HTML.
- C3: slice.html contains zero external resources (no external script, link, or remote img).
- C4: slice.html contains autoplay gating requiring user interaction before speechSynthesis trigger.
- C5: slice.html enforces strict 9:16 aspect ratio on the content wrapper.
- C6: slice.html visual rendering confirms 'Tap to Play' overlay, crude SVG character, and 1 cut.
- C7: slice.html implements mouth animation synced with speech speechSynthesis triggers.
- C8: manifest.md contains valid JSON contract with exact runtime, start overlay, speech settings, and timeline.
- C9: slice.html strictly aligns with constitution.md guidelines.
- C10: slice.html achieves a technical execution score >= 8.0/10 via kit.judge.