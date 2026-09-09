# Manifest

This manifest describes the format and timing schema used for generating video shorts with real-time text-to-speech synthesis using Web Speech API values.

## Delivery Format
- `script.json`: Primary data container.
- `manifest.md`: Schema, instructions, and integration overview.

## JSON Schema

```json
{
  "scenes": [
    {
      "id": 1,
      "description": "Description of scene"
    }
  ],
  "dialogue": [
    {
      "character": "Character Name",
      "text": "Text spoken by character",
      "pitch": 1.0,
      "rate": 1.0,
      "offset_ms": 0
    }
  ]
}
```

### Field Specifics
- `pitch`: Decimal multiplier [0.1, 2.0] used for character speech. Non-uniform values differentiate speakers.
- `rate`: Decimal multiplier [0.5, 2.0] representing spoken velocity.
- `offset_ms`: Cumulative timing markers that orchestrate when dialogues trigger in the overall presentation runtime.
