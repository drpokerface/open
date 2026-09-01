# Deliverable Manifest

## Input Dependencies
- `inputs/script_peter_brian_v3.txt` (original satirical comedy script text, fully proofread)
- `inputs/voiceover_peter_brian_mono_48k.wav` (high-fidelity voice lines in 48kHz WAV format)
- `inputs/character_assets_peter_brian_vector.svg` (fully-layered character vector designs and rigging assets)

## Output Deliverables
- `outputs/final_peter_brian_satirical_reel_916_1080x1920.mp4` (vertical video, 1080x1920 resolution, 9:16 aspect ratio, H.264 codec, max 120s)
- `outputs/audio_stem_dialogue_stereo.wav` (isolated crisp dialogue track for mix adjustments)
- `outputs/audio_stem_sfx_stereo.wav` (isolated sound effects track including timing cues)
- `outputs/audio_stem_music_stereo.wav` (isolated background instrumental track)
- `manifest.md` (this validation manifest file)

## Validation
Producers must ship manifest.md next to their deliverable; Consumers must OPEN and VALIDATE inputs against this manifest before building, rejecting incomplete or rotten inputs via swarm channel. Mock, stub, or incomplete content anywhere in the inputs or outputs is an automatic FAIL.
