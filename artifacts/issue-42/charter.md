# charter.md - this task's charter (turn 0, strong model): every item [assumed] until a probe confirms it; adds to the laws, never relaxes them
packs: code, perception, judging

## Interpretation
[assumed] Goal: Build a completely local Python-based video generation pipeline to produce a 10s MP4 slice (1080x1920, 24fps) demonstrating procedurally drawn geometric shapes, local TTS audio, and one cutaway. Constraints: Strictly programmatic, NO cloud media APIs. Output is tracer_slice.zip. The previous run stalled due to timeout, meaning we must prioritize a rapid end-to-end mechanical slice before subjective tuning.

## Coverage table (one row = one claim in criteria.md = one typed check in verify.py; file | field or constraint | requirement | check)
- tracer_slice.zip | structure | contains capabilities.md, script, slice.mp4, manifest.md | zipfile.ZipFile namelist check.
- slice.mp4 | video specs | 1080x1920 resolution, 24 fps | moviepy.editor.VideoFileClip.size and .fps.
- slice.mp4 | duration | between 9 and 12 seconds | moviepy.editor.VideoFileClip.duration.
- slice.mp4 | animation and cutaway | frames change and show geometric character | kit.perceive on 4 extracted frames spaced evenly.
- slice.mp4 | dialogue | contains TTS audio | kit.perceive on extracted .wav audio and volume threshold check.
- capabilities.md | constraint | verifies programmatic local assembly only | kit.judge confirms no cloud APIs.
- manifest.md | integration | lists exact filenames and formats | kit.judge compares against zipfile namelist.
- slice.mp4 | subjective quality | >= 7/10 on constitution.md rubric | kit.judge on extracted frames, audio transcript, and script text.

## Strategy
[assumed] 1. Turn 1-2: Create degenerate twins for tracer_slice.zip (missing files, wrong dimensions, silent mp4) and write criteria.md. 2. Turn 3: Write verify.py using verify_kit, extracting frames/audio with moviepy, and run it RED. 3. Turn 4: Probe local TTS (pyttsx3) and video (moviepy, Pillow) capabilities to generate capabilities.md. 4. Turn 5-8: Write build_slice.py to draw geometric frames via Pillow and synthesize audio, compiling to slice.mp4. 5. Turn 9-12: Use gemini-3.1-pro-preview via metered to refine timing (3s hook, 5s laugh) against constitution.md. 6. Turn 13: Package tracer_slice.zip and pass verify.py.

## Risks and cheap probes
[assumed] 1. Missing ffmpeg or espeak dependencies break moviepy/pyttsx3. Probe: Turn 1 pip install moviepy pyttsx3 Pillow and render a 1s video with a beep. 2. Perception tools fail on MP4 files. Probe: Ensure verify.py extracts PNG frames and a WAV file from the MP4 using moviepy before calling kit.perceive. 3. Subjective humor bar fails on a short slice. Probe: Explicitly hardcode a stark visual escalation at the 5-second mark in build_slice.py to guarantee the cutaway is perceived.

## Candidate twins (write them under twins/ on turn 1 or 2)
- Missing files: Zip lacks capabilities.md, build_slice.py, slice.mp4, or manifest.md.
- Wrong dimensions: slice.mp4 is 1920x1080 or not 24fps.
- No audio track: slice.mp4 contains video but silent or missing audio track.
- Static video: Extracted frames are identical (no cutaway or animation).
- Non-geometric/Cloud: kit.perceive detects photographic elements instead of drawn shapes, or capabilities.md admits API usage.

## Task rules (add to the laws; never relax them)
- [assumed] 1. TTS must be programmatic and local: attempt pyttsx3 first, fallback to gTTS, but strictly verify no cloud API keys are needed.
- [assumed] 2. verify.py must extract frames and audio manually via python (moviepy/cv2) rather than relying on ffmpeg CLI.
- [assumed] 3. build_slice.py must be deterministic and fully included in the output zip; the deliverable must not rely on manual assembly.
