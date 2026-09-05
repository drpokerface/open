# charter.md - this task's charter (turn 0, strong model): every item [assumed] until a probe confirms it; adds to the laws, never relaxes them
packs: code, perception, judging

## Interpretation
[assumed] The ~10-second slice requirement overrides the 45-119s final convention for this specific task. 'Local Python tools' explicitly allows gTTS and moviepy, meaning no metered cloud APIs like OpenAI or Gemini may be used for media generation, only local libs. All drawing must be programmatic via Pillow or moviepy primitives. We must parse artifacts/board-20260905-100213/constitution.md for the judging rubric.

## Coverage table (one row = one claim in criteria.md = one typed check in verify.py; file | field or constraint | requirement | check)
- tracer_slice.zip | extraction | ZIP archive extracts successfully | zipfile.ZipFile.testzip()
- tracer_slice.zip | contents | contains capabilities.md, build_slice.py, slice.mp4, manifest.md | zipfile.ZipFile.namelist() inclusion
- manifest.md | contents | lists exact filenames and formats | parse markdown and assert required files match namelist
- capabilities.md | content | confirms no cloud APIs used and lists python libs | read text, kit.has_all() for moviepy, gTTS and no cloud APIs
- slice.mp4 | resolution | strictly 1080x1920 (9:16) portrait | moviepy VideoFileClip.size == [1080, 1920]
- slice.mp4 | framerate | exactly 24 fps | moviepy VideoFileClip.fps == 24
- slice.mp4 | duration | ~10 seconds (9-15s) | moviepy VideoFileClip.duration in range
- slice.mp4 | perceptual content | depicts geometric character, has audio dialogue, no complex hallucinated visuals | kit.perceive() on extracted frames and audio clip
- slice.mp4 | subjective quality | score >= 7/10 against Goal Constitution rubric | kit.judge() against artifacts/board-20260905-100213/constitution.md text

## Strategy
[assumed] 1. Write probe script to check availability of moviepy, gTTS, pyttsx3, Pillow, and ffmpeg, saving results to capabilities.md. 2. Define criteria.md and a fully sealed verify.py that unpacks the zip, reads manifest.md, and uses gemini-3.5-flash via kit.perceive on the MP4 to judge the subjective 7/10 bar. 3. Write build_slice.py to generate 10s of geometric animation, synthesize a TTS line, and mix them into slice.mp4. 4. Zip the 4 required files into tracer_slice.zip.

## Risks and cheap probes
[assumed] Risk 1: moviepy fails to write MP4 due to missing ffmpeg binary; Probe: immediately attempt to write a 1-second 10x10 pure black MP4. Risk 2: gTTS fails due to network/API blocks, or pyttsx3 fails due to missing system drivers (espeak); Probe: run a minimal TTS generation script to a .wav file. Risk 3: Perception call cannot process the MP4 format natively; Probe: extract one frame and the audio track and pass them to kit.perceive instead of the raw MP4.

## Candidate twins (write them under twins/ on turn 1 or 2)
- Empty zip: tracer_slice.zip is an empty archive (checks file existence and ZIP extractability).
- Missing files: ZIP extracts but lacks slice.mp4 or capabilities.md (checks manifest match).
- Degenerate MP4: slice.mp4 is 0 bytes or corrupted (checks decode/probe).
- Blank video: MP4 decodes but all frames are solid black (checks kit.perceive visual content).
- Silent video: MP4 has no audio track or 0dB silence (checks audio stream extraction/perception).
- Wrong resolution: MP4 is 1920x1080 landscape instead of 1080x1920 portrait (checks moviepy metadata).

## Task rules (add to the laws; never relax them)
- [assumed] Override the 45-119s duration convention: this probe must be exactly 10-15 seconds.
- [assumed] Never use metered API calls to generate the media itself (video/audio); only use them in verify.py for perception and judging.
- [assumed] Use the provided artifacts/board-20260905-100213/constitution.md as the exact rubric text in your kit.judge calls.
