# charter.md - this task's charter (turn 0, strong model): every item [assumed] until a probe confirms it; adds to the laws, never relaxes them
packs: code, perception, judging

## Interpretation
[assumed] Generate a ~10-second vertical (1080x1920) tracer slice MP4 (`tracer_slice.mp4`) to prove programmatic video generation (Python, Pillow, moviepy, numpy) can create synchronized beep-narration, kinetic typography, and geometric characters, including one visual cutaway. Concurrently, probe for external generation tools and document findings in `capabilities.md`, and define an integration contract in `manifest.md`.

## Strategy
[assumed] 1) Write `criteria.md` and set up twin directories. 2) Write `verify.py` (sealed early), using `gemini-3.5-flash` for perceptual checks (extracting MP4 frames first) to verify geometric shapes, text sync, cutaway presence, and a score >= 8.0. 3) Probe rendering speed by generating a 1-second, 2-frame test video. 4) Probe audio generation by synthesizing a 1-second beep with `numpy`. 5) Write `generate_video.py` using `Pillow` for drawing, `numpy` for beeps, and `moviepy` to assemble the 10-second `tracer_slice.mp4`. 6) Write `manifest.md` and `capabilities.md`. 7) Run `generate_video.py`, then use judged loops to tweak timing and aesthetics until `verify.py` passes.

## Risks and cheap probes
[assumed] 1) Render Timeouts: moviepy rendering 1080x1920 might hit turn time limits. Probe: render a tiny 1-second test video first to measure seconds-per-frame. 2) Perception Failure: the model might not recognize crude shapes as 'characters' or detect the cutaway. Probe: render one frame of the geometric setup, extract it, and ask gemini-3.5-flash what it sees. 3) Audio Sync: syncing numpy beeps with video frames might drift. Probe: create a 2-second clip with two text words and two beeps to verify alignment.

## Candidate twins (write them under twins/ on turn 1 or 2)
- corrupt_mp4: A text file renamed to .mp4 that cannot be decoded (fails mechanical decode).
- short_clip: A correctly formatted video that is only 3 seconds long (fails duration check).
- silent_shapes: A 10-second video with visuals but no audio track or silent audio (fails audio presence/beep check).
- static_blank: A 10-second video of a solid color with audio (fails perceptual check for shapes and kinetic text).
- no_cutaway: A 10-second video with text and shapes but zero scene changes (fails perceptual cutaway check).

## Task rules (add to the laws; never relax them)
- [assumed] Generate all audio mathematically using numpy or standard library wave tools; do not attempt to use any neural TTS APIs.
- [assumed] When verifying the video, extract 3 to 5 specific frames using a Python script or ffmpeg to pass to kit.perceive(), ensuring the model evaluates the final encoded output.
- [assumed] Do not exceed the ~10 second duration for the tracer slice to keep rendering times well within the single-turn budget.
