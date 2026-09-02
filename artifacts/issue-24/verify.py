import os
import sys
import subprocess
import json

try:
    import static_ffmpeg
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'static-ffmpeg'])
    import static_ffmpeg
static_ffmpeg.add_paths()

from verify_kit import Kit
kit = Kit()

def get_metadata(path):
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', path]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(res.stdout)
    except Exception:
        return None

def check_c1():
    return kit.exists('capabilities.md') and kit.exists('manifest.md')

def check_c2():
    if not kit.exists('manifest.md'): return False
    text = kit.text('manifest.md')
    return 'Technical Assertions:' in text and 'Creative Assertions:' in text

def check_c3():
    if not kit.exists('slice.mp4') or os.path.getsize('slice.mp4') == 0:
        return False
    meta = get_metadata('slice.mp4')
    if not meta: return False
    
    fmt = meta.get('format', {})
    dur = float(fmt.get('duration', 0))
    if not (7.0 <= dur <= 15.0):
        return False
        
    has_a = False
    has_v = False
    for s in meta.get('streams', []):
        if s.get('codec_type') == 'audio':
            has_a = True
        elif s.get('codec_type') == 'video':
            has_v = True
            if int(s.get('width', 0)) != 1080 or int(s.get('height', 0)) != 1920:
                return False
            fps_str = s.get('r_frame_rate', '0/1')
            try:
                num, den = map(int, fps_str.split('/'))
                fps = num / den if den > 0 else 0
                if not (11 <= fps <= 16):
                    return False
            except Exception:
                pass
    return has_a and has_v

def check_c4():
    if not kit.exists('slice.mp4'): return False
    os.makedirs('scratch', exist_ok=True)
    frames = []
    for i, t in enumerate([2, 5, 8]):
        out = f'scratch/f{i}.jpg'
        if os.path.exists(out): os.remove(out)
        subprocess.run(['ffmpeg', '-y', '-ss', str(t), '-i', 'slice.mp4', '-vframes', '1', out], capture_output=True)
        if os.path.exists(out): frames.append(out)
    
    if not frames: return False
        
    ans = kit.perceive('C4', 'Frames show geometric character and text', frames, 
        "Look at the frames. Do they clearly show a flat, geometric character (e.g., a circle/polygon with thick outlines) WITH burned-in text subtitles? Reply 'yes' or 'no'.")
    return 'yes' in ans.lower()

rubric = '''
Evaluate the comedy script and execution plan.
Dimension 1: Comedic Tone and Satirical Irreverence
Score 9: Hilarious, boundary-pushing, rapid escalation, clear cutaway gag.
Score 7: Moderately funny, identifiable setup/punchline.
Score 4: Boring, corporate, generic AI humor.

Dimension 2: Vertical Pacing and Retention Mechanics
Score 9: Relentlessly paced, hook in 1-2s, dynamic pacing.
Score 7: Good pacing, occasional pauses.
Score 4: Sluggish, long silence.
'''
anchors = "Baseline 6: A bland script about sliding colored blocks with generic dialogue."

kit.check('C1', 'Capabilities and Manifest exist', check_c1)
kit.check('C2', 'Manifest contains required assertions', check_c2)
kit.check('C3', 'MP4 is valid 1080x1920, 12-15fps, ~10s duration', check_c3)
kit.check('C4', 'Perceptual: visuals match requirements', check_c4)
kit.judge('C5', 'Quality >= 8.0 on GOAL CONSTITUTION', 'manifest.md', rubric, anchors, threshold=8.0)

kit.fault_proof('slice.mp4')
kit.verdict()
