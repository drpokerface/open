# verify_kit.py - VALIDATED: the standard verifier kit - compose checks on it; edit checks, never the kit
import os, sys, json, random, statistics

class Kit:
    """from verify_kit import Kit; kit = Kit(); kit.check(...); kit.judge(...); kit.fault_proof(...); kit.verdict()"""
    def __init__(self):
        self.checks = []        # (id, claim, fn) - mechanical checks, re-run by fault_proof on a corrupted copy
        self.results = []       # every verdict in order
        self.override = {}      # real path -> corrupted copy, only during fault_proof
        os.makedirs("scratch", exist_ok=True)

    # ---- reading: always through these, so fault_proof can swap in the corrupted copy
    def path(self, p):
        return self.override.get(p, p)
    def exists(self, p):
        return os.path.isfile(self.path(p))
    def raw(self, p):
        return open(self.path(p), "rb").read() if self.exists(p) else b""
    def text(self, p):
        try:
            return self.raw(p).decode("utf-8")
        except UnicodeDecodeError:
            return ""
    def size(self, p):
        return len(self.raw(p))
    def no_placeholders(self, p, words=("todo", "tbd", "placeholder", "lorem ipsum", "[insert", "stub", "fixme", "xxx")):
        t = self.text(p).lower()
        found = [w for w in words if w in t]
        return (t.strip() != "" and found == [], ("placeholders found: " + ", ".join(found)) if found else ("clean, " + str(len(t)) + " chars"))
    def has_all(self, p, needles):
        t = self.text(p).lower()
        missing = [n for n in needles if n.lower() not in t]
        return (missing == [], ("missing: " + ", ".join(missing)) if missing else ("all " + str(len(needles)) + " present"))
    def count(self, p, needle):
        return self.text(p).lower().count(needle.lower())
    def min_length(self, p, chars):
        n = len(self.text(p))
        return (n >= chars, str(n) + " chars (floor " + str(chars) + ")")
    def manifest_lists(self, manifest, files):
        t = self.text(manifest)
        missing = [f for f in files if f not in t]
        return (t.strip() != "" and missing == [], ("manifest missing: " + ", ".join(missing)) if missing else "manifest lists all " + str(len(files)))

    # ---- mechanical checks
    def check(self, cid, claim, fn):
        """register and run one mechanical check; fn returns bool or (bool, measured value)"""
        self.checks.append((cid, claim, fn))
        ok, measured = self._run(fn)
        self.results.append(ok)
        print(cid + ": " + ("PASS" if ok else "FAIL") + " - " + claim + " - measured: " + str(measured)[:200])
        return ok
    def _run(self, fn):
        try:
            r = fn()
            if isinstance(r, tuple):
                return bool(r[0]), r[1]
            return bool(r), r
        except Exception as e:
            return False, "check crashed: " + repr(e)[:160]

    # ---- the strongest model this key actually serves (capabilities.json is the attested truth)
    def strongest(self):
        try:
            led = json.load(open("capabilities.json", encoding="utf-8"))
            live = [k for k, v in led.get("models", {}).items() if v.get("ok")]
            return next((k for k in live if "pro" in k), live[0] if live else "gemini-3.5-flash")
        except Exception:
            return "gemini-3.5-flash"

    # ---- the judge: fresh, blind, anchored, sampled, logged
    def judge(self, cid, claim, p, rubric, anchors, threshold=8.0, margin=0.5, samples=3, model=None, baseline=""):
        from metered import generate
        model = model or self.strongest()
        schema = {"type": "object", "required": ["score", "nearest_anchor", "reasoning", "beats_lazy_baseline"], "properties": {
            "score": {"type": "number"}, "nearest_anchor": {"type": "string"}, "reasoning": {"type": "string"}, "beats_lazy_baseline": {"type": "boolean"}}}
        nl = chr(10)
        prompt = ("You are a blind judge. Score the ARTIFACT from 0 to 10 against the RUBRIC, citing the nearest ANCHOR "
                  "and giving one line of reasoning. Also decide whether it clearly beats the laziest acceptable version "
                  "of the same deliverable" + ((" described here: " + baseline) if baseline else "") + ". Judge only what is in front of you."
                  + nl + nl + "RUBRIC:" + nl + rubric + nl + nl + "ANCHORS:" + nl + anchors
                  + nl + nl + "ARTIFACT (" + p + "):" + nl + self.text(p)[:60000])
        scores, beats = [], []
        for i in range(samples):
            try:
                d = json.loads(generate(model, prompt, config={"response_mime_type": "application/json", "response_schema": schema}).text)
                scores.append(float(d.get("score", 0)))
                beats.append(bool(d.get("beats_lazy_baseline")))
                print("  " + cid + " sample " + str(i + 1) + ": " + str(scores[-1]) + " near '" + str(d.get("nearest_anchor", ""))[:60] + "' - " + str(d.get("reasoning", ""))[:180])
            except Exception as e:
                print("  " + cid + " sample " + str(i + 1) + ": judge call failed - " + repr(e)[:140])
        med = statistics.median(scores) if len(scores) == samples else 0.0
        ok = len(scores) == samples and med >= threshold + margin and sum(beats) * 2 > len(beats)
        self.results.append(ok)
        print(cid + ": " + ("PASS" if ok else "FAIL") + " - " + claim + " - measured: median " + str(med) + " of " + str(scores)
              + " vs threshold " + str(threshold) + " + margin " + str(margin) + ", beats lazy baseline " + str(sum(beats)) + "/" + str(len(beats)) + " (model " + model + ")")
        return ok

    # ---- perception: the model looks at media the way the audience will
    def perceive(self, cid, claim, files, question, model="gemini-3.5-flash"):
        from metered import generate, upload
        schema = {"type": "object", "required": ["answer", "seen"], "properties": {"answer": {"type": "boolean"}, "seen": {"type": "string"}}}
        try:
            handles = [upload(self.path(f)) for f in files]
            d = json.loads(generate(model, [question + " Answer true only if what you actually perceive confirms it; describe what you see in 'seen'."] + handles,
                                    config={"response_mime_type": "application/json", "response_schema": schema}).text)
            ok, seen = bool(d.get("answer")), str(d.get("seen", ""))[:200]
        except Exception as e:
            ok, seen = False, "perception call failed - " + repr(e)[:140]
        self.results.append(ok)
        print(cid + ": " + ("PASS" if ok else "FAIL") + " - " + claim + " - seen: " + seen)
        return ok

    # ---- the fault-proof: corrupt a COPY at a random site, prove the mechanical checks catch it
    def fault_proof(self, p, mode=None):
        data = self.raw(p)
        if data == b"":
            print("FAULT-PROOF FAILED: " + p + " is missing or empty - nothing to corrupt")
            self.results.append(False)
            return False
        mode = mode or random.choice(["truncate", "placeholder", "blank"])
        if mode == "blank":
            bad = b""
        elif mode == "truncate":
            bad = data[:random.randint(len(data) // 4, max(len(data) // 2, 1))]
        else:
            try:
                t = data.decode("utf-8")
                site = random.randint(0, len(t))
                bad = (t[:site] + " [PLACEHOLDER - TODO fill this in] " + t[site:]).encode("utf-8")
            except UnicodeDecodeError:
                mode, bad = "truncate", data[:random.randint(len(data) // 4, max(len(data) // 2, 1))]
        copy = os.path.join("scratch", "fault_" + str(random.randint(1000, 9999)) + "_" + os.path.basename(p))
        open(copy, "wb").write(bad)
        self.override[p] = copy
        caught = [cid for cid, claim, fn in self.checks if not self._run(fn)[0]]
        self.override.pop(p, None)
        if caught:
            print("FAULT-PROOF: " + ", ".join(caught) + " caught a random-site " + mode + " fault in " + copy)
            return True
        print("FAULT-PROOF FAILED: no mechanical check caught a " + mode + " fault in " + copy + " - the checks are too weak")
        self.results.append(False)
        return False

    # ---- the last line
    def verdict(self):
        ok = self.results != [] and all(self.results)
        print("VERDICT: " + ("PASS" if ok else "FAIL"))
        sys.exit(0 if ok else 1)
