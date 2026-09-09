import json
import sys
import os
from verify_kit import Kit

kit = Kit()

def check_json_parseable():
    if not kit.no_placeholders('script.json'):
        return False
    try:
        data = json.loads(kit.text('script.json'))
        return True
    except Exception as e:
        print(f"JSON parsing error: {e}")
        return False

def check_schema():
    try:
        data = json.loads(kit.text('script.json'))
        if not isinstance(data, dict):
            return False
        if 'scenes' not in data or 'dialogue' not in data:
            return False
        dialogues = data['dialogue']
        if not isinstance(dialogues, list) or len(dialogues) == 0:
            return False
        for item in dialogues:
            required_keys = ['character', 'text', 'pitch', 'rate', 'offset_ms']
            if not all(key in item for key in required_keys):
                return False
        return True
    except:
        return False

def check_runtime():
    try:
        data = json.loads(kit.text('script.json'))
        offsets = [item['offset_ms'] for item in data['dialogue']]
        if not offsets:
            return False
        max_offset = max(offsets)
        # Runtime must be between 60s (60000ms) and 119s (119000ms)
        print(f"Calculated max offset_ms: {max_offset}")
        return 60000 <= max_offset <= 119000
    except:
        return False

def check_voice_variation():
    try:
        data = json.loads(kit.text('script.json'))
        dialogues = data['dialogue']
        pitches = {item['pitch'] for item in dialogues}
        rates = {item['rate'] for item in dialogues}
        print(f"Unique pitches: {pitches}, unique rates: {rates}")
        return len(pitches) > 1 or len(rates) > 1
    except:
        return False

def check_original_ip():
    try:
        text_content = kit.text('script.json').lower()
        forbidden = ['cartman', 'kyle', 'stan', 'kenny', 'stewie', 'peter griffin', 'brian griffin', 'lois griffin', 'quagmire', 'homer', 'marge', 'bart', 'lisa', 'south park', 'family guy', 'simpsons']
        for f in forbidden:
            if f in text_content:
                print(f"Found forbidden copyrighted reference: {f}")
                return False
        return True
    except:
        return False

def check_manifest():
    if not kit.exists('manifest.md'):
        return False
    manifest_content = kit.text('manifest.md')
    return kit.has_all('manifest.md', ['```json', 'pitch', 'offset_ms'])

kit.check("C1", "script.json is parseable", check_json_parseable)
kit.check("C2", "script.json complies with schema", check_schema)
kit.check("C3", "runtime is between 60s and 119s", check_runtime)
kit.check("C4", "voice parameters show variation", check_voice_variation)
kit.check("C5", "no copyrighted names are used", check_original_ip)
kit.judge(
    "C6",
    "subjective comedy quality is >= 8",
    "script.json",
    kit.text('artifacts/board-20260909-090123/constitution.md'),
    "comedy, sharp edge, escalating absurdity, original characters",
    threshold=8
)
kit.check("C7", "manifest.md exists and contains schema description", check_manifest)

kit.fault_proof('script.json')
kit.verdict()
