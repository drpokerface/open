# charter.md - this task's charter (turn 0, strong model): every item [assumed] until a probe confirms it; adds to the laws, never relaxes them
packs: code, perception, judging

## Interpretation
[assumed] We must synthesize video and audio purely programmatically. Ambiguity: the environment says ffmpeg=NO but also lists it as usable. Decision: We assume CLI ffmpeg is present but will probe immediately; if absent, we fall back to OpenCV cv2.VideoWriter. Characters will be constructed via Python PIL/Pillow as simple colored polygons with thick black outlines. Burned-in subtitles will be drawn directly onto the PIL frames. Audio will use a Python TTS library like gTTS or pyttsx3, stitched into the final mp4.

## Strategy
[assumed] 1. Execute a python script to probe for ffmpeg, cv2, PIL, gTTS, pyttsx3, and moviepy, writing results to capabilities.md. 2. Write criteria.md and verify.py, splitting claims into mechanical (duration 10s, audio/video streams exist, 1080x1920) and perceptual (extracted frames show geometric character and subtitles, judged >8.0 by gemini-3.1-pro-preview based on the constitution). 3. Create manifest.md defining the pipeline data formats. 4. Generate the audio track. 5. Generate 120 frames (10s at 12fps) with PIL, saving to a scratch directory. 6. Mux frames and audio into slice.mp4. 7. Iterate based on verify.py failures.

## Risks and cheap probes
[assumed] 1. ffmpeg is missing despite catalog. Probe: Run subprocess.run(['ffmpeg', '-version']) on turn 1. 2. Python TTS packages are missing. Probe: Try importing gtts or pyttsx3; if absent, generate a basic sine wave, document the gap in capabilities.md, and optionally PROPOSE-PROVIDER for a TTS API. 3. Rendering timeouts. Probe: Benchmark rendering 10 frames with PIL to ensure 120 frames will not breach the loop timeout.

## Candidate twins (write them under twins/ on turn 1 or 2)
- twins/empty_file: A 0-byte slice.mp4 (fails metadata and file size check).
- twins/no_audio: A valid mp4 but missing the audio stream (fails stream count check via ffprobe or cv2).
- twins/static_frame: A 10-second video of a single unchanging frame without subtitles (fails perception check for animation and text).
- twins/realistic_style: A video containing high-fidelity real-world images instead of flat geometric shapes (fails constitution rubric).
- twins/too_short: A compliant video that is only 2 seconds long (fails 10-second duration check).

## Task rules (add to the laws; never relax them)
- [assumed] Video perception claims must extract exactly 3 frames (beginning, middle, end) as JPGs to pass to gemini-3.5-flash for visual verification.
- [assumed] Never attempt to upload the entire MP4 to the model; only upload extracted representative frames and the text transcript.
- [assumed] The first iteration of slice.mp4 must be built by turn 10, even if it is just a red circle bouncing with a single beep, to secure the end-to-end node contract.
