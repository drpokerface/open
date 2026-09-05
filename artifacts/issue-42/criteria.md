## Interpretation
Goal: Build a 10-second end-to-end MP4 video slice testing programmatic compilation without cloud APIs, zipped with source and docs into `tracer_slice.zip`.

## Criteria
- **C1 (Zip structure)**: `tracer_slice.zip` exists, extracts successfully, and its namelist contains exactly `capabilities.md`, `build_slice.py`, `slice.mp4`, and `manifest.md`.
- **C2 (Video specs)**: `slice.mp4` is 1080x1920 resolution, 24 fps.
- **C3 (Duration)**: `slice.mp4` is between 9.0 and 12.0 seconds long.
- **C4 (Visuals & Cutaway)**: Extracted frames change over time, showing flat bold colors, geometric primitives (crude minimalism), sans-serif bold text, and at least one cutaway (absurd escalation at ~8-10s).
- **C5 (Audio)**: Extracted audio contains an audible local TTS audio track with distinct dialogue.
- **C6 (Constraints)**: `capabilities.md` and `build_slice.py` confirm no cloud media APIs were used (only local tools).
- **C7 (Manifest)**: `manifest.md` lists the exact files in the zip and explains their formats accurately.
- **C8 (Quality)**: Subjective quality >= 7/10 against the Goal Constitution's anchored rubric.
