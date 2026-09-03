import os
import sys
import math
import numpy as np

# Monkeypatch numpy to support generators in stacking/concatenation (fixing moviepy + numpy 2.x bug)
import numpy as np
for name in ['vstack', 'hstack', 'concatenate']:
    if hasattr(np, name):
        orig = getattr(np, name)
        def make_patched(orig_func):
            def patched(tup, *args, **kwargs):
                if not isinstance(tup, (list, tuple)) and hasattr(tup, '__iter__'):
                    try:
                        tup = list(tup)
                    except Exception:
                        pass
                return orig_func(tup, *args, **kwargs)
            return patched
        setattr(np, name, make_patched(orig))

try:
    import moviepy.editor as mpy
except ImportError:
    print("moviepy not installed", file=sys.stderr)
from verify_kit import Kit

def run_verify():
    kit = Kit()
    
    kit.check("C1", "capabilities.md exists and has content", 
              lambda: kit.exists("capabilities.md") and len(kit.text("capabilities.md")) > 50)
              
    def check_manifest():
        if not kit.exists("manifest.md"): return False
        t = kit.text("manifest.md")
        req = ["component_id", "duration_ms", "scene_count", "humor_mechanics", "file_dependencies"]
        return all(r in t for r in req)
    kit.check("C2", "manifest.md contains required keys", check_manifest)
    
    def check_duration():
        p = kit.path("tracer_slice.mp4")
        if not os.path.exists(p): return False
        try:
            clip = mpy.VideoFileClip(p)
            return 9.0 <= clip.duration <= 12.0
        except Exception:
            return False
    kit.check("C3", "tracer_slice.mp4 exists, decodable, duration 9-12s", check_duration)
    
    def check_audio():
        p = kit.path("tracer_slice.mp4")
        if not os.path.exists(p): return False
        try:
            clip = mpy.VideoFileClip(p)
            if clip.audio is None: return False
            audio_array = clip.audio.to_soundarray()
            rms = np.sqrt(np.mean(audio_array**2))
            return rms > 0.01
        except Exception:
            return False
    kit.check("C4", "tracer_slice.mp4 has audible audio track", check_audio)
    
    scratch_dir = kit.path("scratch")
    os.makedirs(scratch_dir, exist_ok=True)
    frames_extracted = []
    p = kit.path("tracer_slice.mp4")
    if os.path.exists(p):
        try:
            clip = mpy.VideoFileClip(p)
            d = clip.duration
            times = [d*0.1, d*0.5, d*0.9]
            for i, t in enumerate(times):
                frame = clip.get_frame(t)
                import cv2
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                rel_path = f"scratch/frame_{i}.jpg"
                out_path = kit.path(rel_path)
                cv2.imwrite(out_path, frame_bgr)
                frames_extracted.append(rel_path)
        except Exception:
            pass
            
    if not frames_extracted:
        rel_path = "scratch/dummy.jpg"
        out_path = kit.path(rel_path)
        import cv2
        cv2.imwrite(out_path, np.zeros((100,100,3), dtype=np.uint8))
        frames_extracted = [rel_path]
        
    manifest_text = kit.text("manifest.md")[:1000] if kit.exists("manifest.md") else ""
    q = f"Do these frames depict geometric shapes, kinetic text, and a visually jarring cutaway? Also, does the text in the frames match the comedic intent and script of this manifest sample:\n\n{manifest_text}\n\nAnswer 'yes' or 'no'."
    kit.perceive("C5", "geometric shapes, text, and cutaway match manifest", frames_extracted, q)
        
    rubric = """
    10: Brilliant programmatic lo-fi satire. Hilarious, razor-sharp script using the geometric/kinetic aesthetic as part of the joke. Shocking cutaway perfectly timed.
    8: Funny, fast-paced, includes a jarring cutaway and clever script suitable for a lo-fi geometric style. Subversive and not generic.
    5: Mediocre humor, safe or generic. Cutaway is present but not funny. Feels like standard corporate humor.
    2: Boring, completely literal, or fails to use the medium for humor.
    """
    anchors = """
    "Square realizes he's trapped in a Python array, cuts to a real-life image of a burned out programmer, cuts back to Square screaming in text" - Score: 9
    "Triangle says a generic dad joke about hypotenuses, cuts to a circle" - Score: 4
    """
    kit.judge("C6", "humor >= 8.0", "manifest.md", rubric, anchors, threshold=8.0, model="gemini-3.1-pro-preview", baseline="A safe, generic joke about shapes with a basic cutaway.")
    
    kit.fault_proof("tracer_slice.mp4")
    kit.fault_proof("manifest.md")
    kit.verdict()

if __name__ == "__main__":
    run_verify()
