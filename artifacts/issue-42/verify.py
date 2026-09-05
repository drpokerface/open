import os
import sys
import subprocess
import zipfile
import shutil

# Install dependencies for verification
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "moviepy==1.0.3", "Pillow", "numpy"])

from verify_kit import Kit
kit = Kit()

DELIVERABLE = "tracer_slice.zip"
SCRATCH = "scratch"

def setup_scratch():
    if os.path.exists(SCRATCH):
        shutil.rmtree(SCRATCH, ignore_errors=True)
    os.makedirs(SCRATCH, exist_ok=True)
    if os.path.exists(DELIVERABLE):
        try:
            with zipfile.ZipFile(DELIVERABLE, 'r') as z:
                z.extractall(SCRATCH)
        except zipfile.BadZipFile:
            pass

setup_scratch()

def check_c1():
    expected = ["capabilities.md", "slice.mp4", "manifest.md", "build_slice.py"]
    for f in expected:
        if not os.path.exists(os.path.join(SCRATCH, f)):
            return False
    return True
kit.check("C1", "tracer_slice.zip contains required files", check_c1)

def check_c2():
    try:
        from moviepy.editor import VideoFileClip
        vid_path = os.path.join(SCRATCH, "slice.mp4")
        if not os.path.exists(vid_path): return False
        clip = VideoFileClip(vid_path)
        if clip.w != 1080 or clip.h != 1920: return False
        if abs(clip.fps - 24) > 0.5: return False
        return True
    except Exception:
        return False
kit.check("C2", "slice.mp4 is 1080x1920 and 24fps", check_c2)

def check_c3():
    try:
        from moviepy.editor import VideoFileClip
        vid_path = os.path.join(SCRATCH, "slice.mp4")
        if not os.path.exists(vid_path): return False
        clip = VideoFileClip(vid_path)
        return 9 <= clip.duration <= 13
    except Exception:
        return False
kit.check("C3", "slice.mp4 duration between 9 and 13 seconds", check_c3)

def check_c4():
    try:
        from moviepy.editor import VideoFileClip
        vid_path = os.path.join(SCRATCH, "slice.mp4")
        if not os.path.exists(vid_path): return False
        clip = VideoFileClip(vid_path)
        frames_dir = os.path.join(SCRATCH, "frames")
        os.makedirs(frames_dir, exist_ok=True)
        times = [1.0, 4.0, 7.0, clip.duration - 1.0]
        extracted = []
        for i, t in enumerate(times):
            if t > clip.duration or t < 0: t = clip.duration / 2
            f_path = os.path.join(frames_dir, f"frame_{i}.png")
            clip.save_frame(f_path, t=t)
            extracted.append(f_path)
        return kit.perceive("C4", "Frames change and show geometric character with cutaway", extracted, "Do these frames show procedurally drawn geometric shapes/characters with flat bold colors, and does at least one frame show a distinct cutaway or absurd visual escalation compared to the earlier frames?")
    except Exception:
        return False
kit.check("C4", "Frames change and show geometric character with cutaway", check_c4)

def check_c5():
    try:
        from moviepy.editor import VideoFileClip
        vid_path = os.path.join(SCRATCH, "slice.mp4")
        if not os.path.exists(vid_path): return False
        clip = VideoFileClip(vid_path)
        if clip.audio is None: return False
        aud_path = os.path.join(SCRATCH, "audio.wav")
        clip.audio.write_audiofile(aud_path, logger=None)
        return kit.perceive("C5", "Audio contains TTS dialogue", [aud_path], "Does this audio contain synthesized TTS dialogue (spoken words)?")
    except Exception:
        return False
kit.check("C5", "slice.mp4 contains TTS audio", check_c5)

def check_c6():
    cap_path = os.path.join(SCRATCH, "capabilities.md")
    if not os.path.exists(cap_path): return False
    rubric = "Score 10 if this text strictly confirms local Python tools were used and no cloud media APIs were used. Score 0 if cloud APIs are mentioned as used."
    return kit.judge("C6", "capabilities.md confirms no cloud APIs", cap_path, rubric, "Anchors: Local=10, Cloud=0", threshold=8.0, model=kit.strongest())
kit.check("C6", "capabilities.md confirms no cloud APIs", check_c6)

def check_c7():
    man_path = os.path.join(SCRATCH, "manifest.md")
    if not os.path.exists(man_path): return False
    return kit.manifest_lists(man_path, ["capabilities.md", "slice.mp4", "manifest.md", "build_slice.py"])
kit.check("C7", "manifest.md lists required files", check_c7)

def check_c8():
    script_path = os.path.join(SCRATCH, "build_slice.py")
    if not os.path.exists(script_path): return False
    rubric = kit.text("artifacts/board-20260905-100213/constitution.md")
    return kit.judge("C8", "Quality >= 7/10 against constitution", script_path, rubric, "Anchors: 9=Perfect sharp minimalism and timing. 4=Boring/broken timing.", threshold=7.0, model=kit.strongest())
kit.check("C8", "Subjective quality >= 7/10 on constitution.md rubric", check_c8)

kit.fault_proof(DELIVERABLE)
kit.verdict()
