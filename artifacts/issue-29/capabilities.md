# Capabilities Probe

## Probe Results
- **Text-to-Speech (TTS) APIs**: UNAVAILABLE. No neural TTS tools or keys are active in the environment.
- **Text-to-Video APIs**: UNAVAILABLE. No neural video synthesis is reachable.
- **Image Generation APIs**: UNAVAILABLE. Image generation is restricted by the constitution.

## Programmatic Alternatives (Fully Validated)
- **Video Assembly**: `moviepy` is installed and functioning for sequential frame compilation.
- **Visual Frame Generation**: PIL (`Pillow`) is active. Falling back to programmatic canvas drawing and custom high-contrast, lo-fi pixel font scaling to bypass potential ImageMagick errors.
- **Synthetic Audio Synthesis**: `numpy` and the Python built-in `wave` module are used to generate sample-perfect, phase-continuous sine-wave beeps and sweep buzzer tones.