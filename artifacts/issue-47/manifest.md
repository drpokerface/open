# Manifest

This integration contract outlines the runtime parameters, configuration settings, and structural timeline for the Tracer Slice.

```json
{
  "runtime": "11 seconds",
  "start_overlay": true,
  "speech_settings": {
    "rate": 1.1,
    "pitch": 0.8,
    "voice": "default"
  },
  "timeline": [
    {
      "time": 0.0,
      "event": "interaction_unlocked",
      "action": "The massive magenta full-screen overlay is clicked, dismissing itself and initiating Scene 1. Speech Synthesis Utterance 1 begins speaking the initial dialogue of Gary the suburban homeowner."
    },
    {
      "time": 5.0,
      "event": "scene_cut",
      "action": "Scene 1 is dynamically hidden, Scene 2 is displayed, representing a visual cut. Speech Synthesis is cleared, and Speech Synthesis Utterance 2 begins speaking Gary's panicked reaction."
    },
    {
      "time": 10.0,
      "event": "narrative_end",
      "action": "All speech synthesis is finished. The animation stops, and the subtitles update to display FIN."
    }
  ]
}
```
