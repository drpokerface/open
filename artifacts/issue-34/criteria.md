# criteria.md - Root claims for the tracer slice

## Interpretation
Given the strict absence of neural media generators, the solution must use client-side browser APIs. Specifically, we use standard inline SVGs for visuals and the native Web Speech API (`window.speechSynthesis`) for character voice generation. 
To avoid browser autoplay blocks, a explicit user interaction (e.g., a Start button) must trigger the voice/animation. The format must be strictly 9:16 vertical (e.g. 1080x1920 scaled via CSS).

## Claims
- C1: `capabilities.md` exists and explicitly details that neural text-to-speech, text-to-video, and image generators are missing or unreachable, justifying the client-side fallback.
- C2: `slice.html` exists and strictly enforces a 9:16 vertical aspect ratio using explicit sizing (such as CSS `aspect-ratio: 9/16` or `width: 1080px; height: 1920px` constraints).
- C3: `slice.html` utilizes the native Web Speech API (`window.speechSynthesis` and `SpeechSynthesisUtterance`) to voice character dialog.
- C4: `slice.html` contains at least one inline SVG element containing basic geometric shapes (`<rect>`, `<circle>`, or `<path>`), representing the character, without using any external raster image or video tags (`<img>`, `<video>`).
- C5: `slice.html` contains an interactive element (e.g., a button with id `start` or text 'start/play') that acts as a user-interaction gate before initiating audio playback.
- C6: `manifest.md` exists and details the file formats, SVG IDs, and the data-passing structure used to sequence the animation.
