# Animation Swarm Manifest

## File Formats
All artifacts are delivered as self-contained HTML5 files. The primary output is `slice.html`, which bundles CSS, ES6 JavaScript, and inline SVGs. There are no external assets.

## SVG IDs
The inline SVGs use specific IDs to allow JavaScript targeting for crude cutout animation:
- `stage` - The main 9:16 aspect ratio container.
- `char-head` - The upper half of the head for South Park-style talking.
- `char-mouth` - The mouth element.
- `char-body` - The torso.

## Animation Sequencing Structure and Data-Passing
The animation is sequenced using a data-passing structure defined as an array of script line objects. The JavaScript engine iterates through this structure, firing the Web Speech API and synchronizing the SVG CSS translations and cutaways to the `SpeechSynthesisUtterance` events (`onstart`, `onend`).

### Tiny Sample Proving the Format
```json
[
  {
    "speaker": "char1",
    "text": "What are we even doing here?",
    "delayBefore": 500
  },
  {
    "speaker": "char2",
    "text": "Executing comedic timing via code, obviously.",
    "delayBefore": 1500
  }
]
```
