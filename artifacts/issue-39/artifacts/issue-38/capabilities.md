# capabilities.md - Browser and Model Capabilities

## Native Browser APIs
- **Speech Synthesis**: Native `window.speechSynthesis` is available inside modern browsers. It executes asynchronously and does not block the main animation thread.
- **Audio/Video APIs**: External API calls are unavailable (no standard TTS, no video/audio generation service). Browser-native audio synthesis is the only speech vehicle.
- **CSS Animation**: High-performance keyframe-based visual updates, suitable for 9:16 layout.

## Attested LLMs (via metered.py)
- **gemini-3.5-flash**: Fast, default model for routine checks and code structure parsing.
- **gemini-3.1-pro-preview**: Strong model for subjective evaluation, script quality, and layout scoring.
