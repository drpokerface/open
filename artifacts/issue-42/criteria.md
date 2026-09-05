# criteria.md

## Interpretation
- The task requires `tracer_slice.zip` containing `capabilities.md`, `build_slice.py`, `slice.mp4`, and `manifest.md`.
- `slice.mp4` must be ~10 seconds (9-15s), 1080x1920 (9:16), 24 fps.
- Submissions must be purely programmatic (no cloud APIs for media).
- Quality is judged >= 7/10 against `artifacts/board-20260905-100213/constitution.md`.

## Claims
C1: ZIP archive `tracer_slice.zip` exists and extracts successfully.
C2: Extracted contents include `capabilities.md`, `build_slice.py`, `slice.mp4`, `manifest.md`.
C3: `manifest.md` lists exact filenames.
C4: `capabilities.md` confirms no cloud APIs are used.
C5: `slice.mp4` resolution is strictly 1080x1920 (9:16) portrait.
C6: `slice.mp4` framerate is exactly 24 fps.
C7: `slice.mp4` duration is between 9 and 15 seconds.
C8: `slice.mp4` depicts geometric character, has audio dialogue, no complex hallucinated visuals.
C9: `slice.mp4` subjective quality score >= 7/10 against Goal Constitution rubric.
