import os, sys, cv2
try:
    import moviepy.editor
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy", "numpy", "opencv-python", "pillow"])
    import moviepy.editor

from verify_kit import Kit
kit = Kit()

kit.check("C1", "capabilities.md exists", lambda: (kit.exists("capabilities.md"), "found" if kit.exists("capabilities.md") else "missing"))

def check_manifest():
    if not kit.exists("manifest.md"): return False, "missing"
    t = kit.text("manifest.md")
    missing = [f for f in ["component_id", "duration_ms", "scene_count", "humor_mechanics", "file_dependencies"] if f not in t]
    return (False, "missing fields: "+", ".join(missing)) if missing else (True, "ok")
kit.check("C2", "manifest.md fields", check_manifest)

_c345 = None
def get_c345():
    global _c345
    if _c345 is not None: return _c345
    vp = kit.path("tracer_slice.mp4")
    if not os.path.exists(vp):
        _c345 = (False, "missing", False, "missing", False, "missing")
        return _c345
    try:
        from moviepy.editor import VideoFileClip
        clip = VideoFileClip(vp)
        dur = clip.duration
        c4 = 8 <= dur <= 12
        c5 = clip.audio is not None
        clip.close()
        _c345 = (True, "valid", c4, f"dur {dur}s", c5, "audio present" if c5 else "no audio")
    except Exception as e:
        _c345 = (False, f"err {e}", False, "err", False, "err")
    return _c345

kit.check("C3", "tracer_slice.mp4 exists and valid", lambda: (get_c345()[0], get_c345()[1]))
kit.check("C4", "duration ~10s", lambda: (get_c345()[2], get_c345()[3]))
kit.check("C5", "audio track", lambda: (get_c345()[4], get_c345()[5]))

def extract():
    vp = kit.path("tracer_slice.mp4")
    if not os.path.exists(vp): return []
    cap = cv2.VideoCapture(vp)
    if not cap.isOpened(): return []
    t = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if t <= 0: return []
    os.makedirs(kit.path("scratch"), exist_ok=True)
    paths = []
    for i in range(5):
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, min(t-1, int((i/4.0)*(t-1)))))
        ret, f = cap.read()
        if ret:
            p = kit.path(f"scratch/f{i}.jpg")
            cv2.imwrite(p, f)
            paths.append(f"scratch/f{i}.jpg")
    cap.release()
    return paths

frames = extract()

kit.check("C6", "geometric shapes and typography", lambda: kit.perceive("C6", "geometric shapes and typography", frames, "Does the video show characters constructed from geometric shapes, alongside kinetic typography (large text)? Look at the frames. Reply YES or NO, then reason.") if frames else (False, "no frames"))
kit.check("C7", "visual cutaway", lambda: kit.perceive("C7", "visual cutaway", frames, "Looking at the sequence of frames, is there a visual cutaway to a completely different scene? Reply YES or NO, then reason.") if frames else (False, "no frames"))

rubric = '''
10 - Perfect execution of Programmatic Lo-Fi Minimalism. Striking visual hook, geometry used masterfully, clear cutaway gag.
8 - Great execution. Has a hook, clear geometric aesthetic, and a cutaway.
6 - Passable but flawed. Geometry present, but pacing off. Cutaway is weak.
4 - Failed attempt. Mostly static, lacks clear cutaway, text illegible.
2 - Completely misses the mark.
'''
anchors = '''
10 Anchor: 'South Park Pilot Lo-Fi': Crude cutouts, incredibly fast pacing, distinct cutaways.
8 Anchor: 'Geometric Cynic': Triangles, text slamming on screen, quick cutaway.
4 Anchor: 'Slow Shapes': A square talking slowly, no cutaway, boring.
'''
kit.judge("C8", "quality >= 8", "tracer_slice.mp4", rubric, anchors, threshold=8.0)

kit.fault_proof("tracer_slice.mp4")
kit.verdict()
