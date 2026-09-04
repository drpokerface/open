# capabilities.md - Assessment of Media Generation Capabilities

## 1. Catalog Probe and Status
As of the assessment on 2026-09-04, our active catalog in `providers.md` and available environment variables confirm that:
- **Image Generation:** No external or neural pixel-based image generators are configured or subscribed (unreachable).
- **Text-to-Speech:** No external neural TTS engines (e.g., ElevenLabs, Play.ht) are configured or subscribed (unreachable).
- **Text-to-Video:** No text-to-video generators are configured or subscribed (unreachable).

## 2. Environment Tools
- **ffmpeg:** Disabled / not found in the path (`ffmpeg` field is false in `capabilities.json`).
- **git:** Available (`git` field is true in `capabilities.json`).

## 3. Justification for Fallback Strategy
Given the absolute absence of pixel-based image generators, neural text-to-speech, and neural text-to-video, we must strictly leverage browser-native client APIs and lightweight code-driven assets:
1. **Visuals:** Inline Scalable Vector Graphics (SVG) styled via CSS will represent all characters and backgrounds. This guarantees sharp, scalable, and lightweight rendering at 9:16 aspect ratio without depending on image hosts.
2. **Sound/Voice:** The browser-native Web Speech API (`window.speechSynthesis`) and `SpeechSynthesisUtterance` objects will drive all character dialogue, using custom pitch/rate parameters to differentiate characters.
3. **Timing and Orchestration:** Native ES6 JavaScript promises and event listeners (`onstart`, `onend` on speech utterances) will orchestrate precise visual timing cuts, mouth state changes, and comedic beats without drifting.
