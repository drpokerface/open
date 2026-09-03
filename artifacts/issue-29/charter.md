# charter.md - this task's charter (turn 0, strong model): every item [assumed] until a probe confirms it; adds to the laws, never relaxes them
packs: code, perception, judging

## Interpretation
[assumed] We are building a 10s video ('tracer_slice.mp4') strictly using Python ('moviepy', 'Pillow', 'numpy') because neural media APIs are explicitly prohibited. The video must contain one main geometric scene, one jarring cutaway, and kinetic text synced to synthetic sine-wave 'beeps'. We will output 'capabilities.md' confirming available tools (or lack thereof), and 'manifest.md' defining the slice's specs. 'verify.py' must physically extract frames/audio, using 'gemini-3.5-flash' to verify the geometric visuals, cutaway, and text sync, plus 'gemini-3.1-pro-preview' for the subjective 8.0/10 humor check.

## Strategy
[assumed] 1. Write criteria.md establishing the mechanical tests (duration, file presence) and perceptual tests (cutaway exists, text matches beeps, humor > 8.0). 2. Write verify.py using verify_kit; it must extract 3 keyframes (start, middle, end) and audio RMS levels from tracer_slice.mp4 to feed to the perception and judging models. 3. Execute a quick OS/env probe and write capabilities.md. 4. Write manifest.md. 5. Write generate_slice.py using numpy for audio beeps and moviepy/Pillow for geometric shapes and text. 6. Run the generator to produce a rough video, then iterate purely on sync and cutaway timing until verify.py passes.

## Risks and cheap probes
[assumed] 1. moviepy TextClip fails due to missing ImageMagick: Probe by rendering a 1s TextClip immediately; if it fails, fallback to drawing text on frames with Pillow. 2. Verifier hallucinating success on degenerate video: Probe by passing an all-black frame array to the perception check to ensure the model explicitly rejects it. 3. Audio generation stalling: Probe by generating a simple 1s 440Hz sine wave via numpy and saving as audio to confirm format compatibility.

## Candidate twins (write them under twins/ on turn 1 or 2)
- A perfectly 10s video that is a solid color with no text or cutaway.
- A 10s video with text and shapes, but a completely silent audio track.
- A video containing beeps and text, but remaining in a single scene with no cutaway.
- A video with all elements but truncated to 3 seconds.
- A fully featured video whose humor and script are painfully generic and safe (fails subjective >8.0).

## Task rules (add to the laws; never relax them)
- [assumed] Use numpy to generate raw audio arrays for the synthetic beeps; do not waste time searching for missing TTS packages.
- [assumed] For video perception checks, extract exactly three frames (one early, one mid/cutaway, one late) and send them as a single multi-image prompt to gemini-3.5-flash.
- [assumed] If moviepy TextClip throws OS-level ImageMagick errors, do not attempt to debug the environment; instantly pivot to rendering text frame-by-frame using Pillow.
