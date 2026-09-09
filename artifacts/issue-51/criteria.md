# Criteria

## Interpretation
We verify that the video tracer slice (slice.html) and its metadata files (capabilities.md, manifest.md) meet all strict container, visual, audio, and script timing/comedic pacing rules outlined in the charter and constitution. The video must run purely in the browser using HTML5/CSS/JS with inline SVG elements, and browser window.speechSynthesis API for audio narration.

## Claims

### C1: Tool Probe
- **Claim**: `capabilities.md` explicitly notes the absence of text-to-video and text-to-speech tools.
- **Check**: Read `capabilities.md` and check for explicit mentions of the lack/absence of text-to-speech and text-to-video tools.

### C2: Manifest Headers
- **Claim**: `manifest.md` contains headers for Asset Manifestation, Timeline Cues, and Voice Profiles.
- **Check**: Read `manifest.md` and check that the strings "Asset Manifestation", "Timeline Cues", and "Voice Profiles" are all present.

### C3: Voice Profiles
- **Claim**: `manifest.md` voice profiles specify pitch between 0.0 and 2.0, and rate between 0.1 and 10.0.
- **Check**: Parse the file for pitch and rate settings to verify they are floats within those ranges.

### C4: Interactive Start
- **Claim**: `slice.html` contains an interactive Play button to bypass browser autoplay blocks.
- **Check**: Parse/search HTML for a button tag with an id or class representing 'play' or with content/attribute for 'play'.

### C5: Container Constraints
- **Claim**: `slice.html` CSS enforces aspect-ratio 9/16, max-width 1080px, and max-height 1920px.
- **Check**: Parse style tags/attributes or CSS rules in `slice.html` to ensure aspect-ratio 9/16 (or 9 / 16) and max-width 1080px and max-height 1920px constraints are set.

### C6: Media Independence
- **Claim**: `slice.html` has zero external media files (no img src external, no audio src, no video tags).
- **Check**: Inspect file contents to confirm absence of `<img`, `<audio`, `<video` with external URLs (excluding standard inline SVG components).

### C7: Subtitles
- **Claim**: `slice.html` has a kinetic typography overlay container for subtitles.
- **Check**: Parse file for a dedicated container or div for subtitles/captions.

### C8: Narration
- **Claim**: `slice.html` uses `window.speechSynthesis` API or `speechSynthesis.speak` for audio narrative sync.
- **Check**: Search JS contents for `speechSynthesis` usage.

### C9: Comedic Cutaway Impact
- **Claim**: The comedic timing, script, and visual cutaway cues in `slice.html` and `manifest.md` score >= 8.0/10.
- **Check**: `kit.judge` evaluates the script quality and comedic timing against the Rubric and Anchors.
