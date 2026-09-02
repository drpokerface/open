# Criteria for Tracer Slice

## Interpretation
We must generate a programmatic video slice (`slice.mp4`) that mimics the South Park style.
It must be an H.264/AAC MP4, 1080x1920 (9:16), 12-15 fps, ~10s in length.
It must contain burned-in subtitles and flat geometric characters.
Audio is generated via TTS.

## Claims
C1: `capabilities.md` and `manifest.md` exist.
C2: `manifest.md` contains YAML asset manifest, Technical Assertions, and Creative Assertions.
C3: `slice.mp4` exists, duration is 7-15s, video is 1080x1920 at 12-15fps, has audio and video streams.
C4: Perceptual: 3 extracted frames show geometric characters and subtitles.
C5: Subjective: The script and pacing described in manifest.md achieve a score of >= 8.0 on the rubric.
