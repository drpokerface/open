import os
import sys
import subprocess
import zipfile
import shutil

try:
    import moviepy.editor as mp
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy==1.0.3", "Pillow", "numpy", "imageio==2.4.1", "decorator==4.4.2", "imageio-ffmpeg==0.4.9"])
    import moviepy.editor as mp

from verify_kit import Kit
kit = Kit()

def extract_zip():
    if os.path.exists("scratch/extracted"):
        shutil.rmtree("scratch/extracted")
    os.makedirs("scratch/extracted", exist_ok=True)
    try:
        with zipfile.ZipFile("tracer_slice.zip", 'r') as zip_ref:
            zip_ref.extractall("scratch/extracted")
        return True
    except Exception:
        return False

kit.check("C1", "ZIP archive extracts successfully", lambda: kit.exists("tracer_slice.zip") and extract_zip())

req_files = ["capabilities.md", "build_slice.py", "slice.mp4", "manifest.md"]
kit.check("C2", "Extracted contents include required files", lambda: all(os.path.exists(f"scratch/extracted/{f}") for f in req_files))

def check_c3():
    try:
        text = open("scratch/extracted/manifest.md").read()
        return all(f in text for f in req_files)
    except: return False
kit.check("C3", "manifest.md lists exact filenames", check_c3)

def check_c4():
    try:
        text = open("scratch/extracted/capabilities.md").read().lower()
        if "moviepy" not in text: return False
        if "no cloud api" not in text and "no cloud media api" not in text: return False
        return True
    except: return False
kit.check("C4", "capabilities.md confirms no cloud APIs are used", check_c4)

def get_clip():
    try:
        return mp.VideoFileClip("scratch/extracted/slice.mp4")
    except Exception:
        return None

def check_c5():
    clip = get_clip()
    if not clip: return False
    return list(clip.size) == [1080, 1920]
kit.check("C5", "slice.mp4 resolution is strictly 1080x1920", check_c5)

def check_c6():
    clip = get_clip()
    if not clip: return False
    return abs(clip.fps - 24) < 0.1
kit.check("C6", "slice.mp4 framerate is exactly 24 fps", check_c6)

def check_c7():
    clip = get_clip()
    if not clip: return False
    return 9 <= clip.duration <= 15
kit.check("C7", "slice.mp4 duration is between 9 and 15 seconds", check_c7)

if os.path.exists("scratch/derivative.txt"):
    os.remove("scratch/derivative.txt")

def check_c8():
    try:
        clip = mp.VideoFileClip("scratch/extracted/slice.mp4")
        os.makedirs("scratch", exist_ok=True)
        clip.save_frame("scratch/frame.png", t=min(clip.duration/2, clip.duration-0.1))
        media = ["scratch/frame.png"]
        if clip.audio:
            clip.audio.write_audiofile("scratch/audio.wav", logger=None)
            media.append("scratch/audio.wav")
            
        ans = kit.perceive("C8_percept", "depicts geometric character and contains audio dialogue", media, "Does the image depict a minimal geometric character without hallucinated visuals, and does the audio contain clear dialogue? Answer YES or NO.")
        
        desc = kit.perceive("C9_desc", "describe the video for judging", media, "Describe the visual style, characters, humor, escalation, timing, and TTS audio of this video in detail based on the provided frame and audio.")
        with open("scratch/derivative.txt", "w", encoding="utf-8") as f:
            f.write(desc if desc else "Description failed.")
            
        return bool(ans)
    except Exception as e:
        os.makedirs("scratch", exist_ok=True)
        with open("scratch/derivative.txt", "w", encoding="utf-8") as f:
            f.write("Extraction failed.")
        return False
kit.check("C8", "slice.mp4 depicts geometric character, has audio dialogue", check_c8)

rubric_text = kit.text("artifacts/board-20260905-100213/constitution.md")
if not rubric_text:
    rubric_text = "Fallback rubric: minimal geometric style, 3s hook, 5s first laugh, 8-10s escalation."
anchors_text = '''Anchors:
- Exemplar 1 (Score 9): Strong geometric aesthetics, clear hook, hilarious absurd escalation before 10s, TTS sounds distinct.
- Exemplar 2 (Score 4): Basic shapes, TTS audio, but static, lacks humor, no escalation.
- Exemplar 3 (Score 2): Just a circle and robotic voice saying hello, boring.'''
kit.judge("C9", "subjective quality score >= 7/10", "scratch/derivative.txt", rubric_text, anchors_text, threshold=7.0)

kit.fault_proof("tracer_slice.zip")
kit.verdict()
