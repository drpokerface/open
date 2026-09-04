# criteria.md

## Interpretation
- `slice.html` is a zero-dependency programmatic video slice for 9:16 aspect ratio.
- "Not blank, silent, empty, uniform, or truncated" means the file contains substantive content: `<svg>`, `<style>` with `@keyframes`, and `<script>` containing `speechSynthesis`.
- "Perception call" parses the DOM/JS structure to confirm TTS usage, subtitle syncing, cutaway animation, and one line of voiced edgy dialogue.
- Subjective quality is judged against the constitution by sending the whole HTML source to the model.

## Claims
- **C1**: `slice.html` and `manifest.md` exist.
- **C2**: `slice.html` contains `<svg>`, `@keyframes`, and `speechSynthesis`.
- **C3**: `slice.html` contains a 9:16 aspect ratio constraint.
- **C4**: Perceptual - Code contains TTS subtitle synchronization logic and a cutaway transition.
- **C5**: Subjective - Judges score the content >= 8.0 against the constitution.

C6: `capabilities.md` exists, is non-empty, and documents the findings of the capability probe.
