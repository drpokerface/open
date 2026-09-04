# verify_kit.py - VALIDATED: the standard verifier kit - compose checks on it; edit checks, never the kit
# Cost rules (v10.1): the judge defaults to gemini-3.5-flash; pass model=kit.strongest() only where the
# goal demands the strong model. judge() and perceive() are skipped when an earlier check already failed -
# a blank twin must never reach a judge.
# One verdict, one truth (v10.2): the real artifact and the gate always run in full (KIT_MODE=full). The
# loop sets KIT_MODE=cheap ONLY for twin runs, and cheap mode only reduces the judge to one flash sample -
# it never changes WHAT a check looks at. Every verdict line states what the model was actually shown
# (files, chars, model, samples); a check that cannot see its artifact (judge() on a binary or missing
# file, perceive() with no readable files) fails LOUDLY, with the reason, instead of judging nothing.
import os, sys, json, hashlib, statistics

CHEAP = os.environ.get("KIT_MODE", "full") == "cheap"

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
    def _skip(self, cid, claim):
        # fail-fast: a judge or perception call costs money and proves nothing once a mechanical check failed
        if not all(self.results):
            self.results.append(False)
            print(cid + ": FAIL - " + claim + " - skipped: an earlier check already failed (fail-fast, no model call)")
            return True
        return False

    def judge(self, cid, claim, p, rubric, anchors, threshold=8.0, margin=0.5, samples=3, model=None, baseline=""):
        if self._skip(cid, claim):
            return False
        # v10.2 (one verdict, one truth): judge() reads TEXT. A missing or empty artifact fails without a model
        # call; a binary one is a MIS-WIRED check said out loud - never a silent score on an empty string.
        data = self.raw(p)
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = None
        if text is None:
            self.results.append(False)
            print(cid + ": FAIL - " + claim + " - MIS-WIRED CHECK: judge() reads text but " + p + " is binary (not UTF-8), so this check can never pass for ANY artifact"
                  + " - judge a text derivative (transcript, frame descriptions, extracted data) or use kit.perceive() for media (no model call)")
            return False
        if text.strip() == "":
            self.results.append(False)
            print(cid + ": FAIL - " + claim + " - " + p + (" is missing" if not self.exists(p) else " is empty") + ": nothing to judge (no model call)")
            return False
        from metered import generate
        model = model or "gemini-3.5-flash"
        if CHEAP:
            model, samples = "gemini-3.5-flash", 1
        shown = text[:60000]
        schema = {"type": "object", "required": ["score", "nearest_anchor", "reasoning", "beats_lazy_baseline"], "properties": {
            "score": {"type": "number"}, "nearest_anchor": {"type": "string"}, "reasoning": {"type": "string"}, "beats_lazy_baseline": {"type": "boolean"}}}
        nl = chr(10)
        prompt = ("You are a blind judge. Score the ARTIFACT from 0 to 10 against the RUBRIC, citing the nearest ANCHOR "
                  "and giving one line of reasoning. Also decide whether it clearly beats the laziest acceptable version "
                  "of the same deliverable" + ((" described here: " + baseline) if baseline else "") + ". Judge only what is in front of you."
                  + nl + nl + "RUBRIC:" + nl + rubric + nl + nl + "ANCHORS:" + nl + anchors
                  + nl + nl + "ARTIFACT (" + p + "):" + nl + shown)
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
        if CHEAP:
            print("  " + cid + ": cheap mode - this is a TWIN run (one flash sample); the real artifact and the gate always judge in full")
        self.results.append(ok)
        print(cid + ": " + ("PASS" if ok else "FAIL") + " - " + claim + " - measured: median " + str(med) + " of " + str(scores)
              + " vs threshold " + str(threshold) + " + margin " + str(margin) + ", beats lazy baseline " + str(sum(beats)) + "/" + str(len(beats))
              + " - judged " + str(len(shown)) + ((" of " + str(len(text)) + " chars (clipped)") if len(text) > len(shown) else " chars") + " of " + p
              + " with " + model + " x" + str(samples) + (" [cheap twin mode]" if CHEAP else ""))
        return ok

    # ---- perception: the model looks at media the way the audience will
    def perceive(self, cid, claim, files, question, model="gemini-3.5-flash"):
        if self._skip(cid, claim):
            return False
        # v10.2 (one verdict, one truth): every file named is shown, in every mode - the kit never silently
        # narrows what a check looks at - and the verdict line states exactly what the model was shown
        files = [files] if isinstance(files, str) else list(files)
        unreadable = [f for f in files if not self.exists(f) or self.size(f) == 0]
        if files == [] or unreadable != []:
            self.results.append(False)
            print(cid + ": FAIL - " + claim + " - nothing was shown to the model: " + ("no files given" if files == [] else "missing or empty files " + ", ".join(unreadable)[:200])
                  + " (no model call) - extract or render the samples first, then name them here")
            return False
        from metered import generate, upload
        shown = (str(len(files)) + " file" + ("s" if len(files) != 1 else "") + " (" + (files[0] if len(files) == 1 else files[0] + " .. " + files[-1]) + ", "
                 + str(max(1, sum(self.size(f) for f in files) // 1024)) + " KB) to " + model)
        schema = {"type": "object", "required": ["answer", "seen"], "properties": {"answer": {"type": "boolean"}, "seen": {"type": "string"}}}
        try:
            handles = [upload(self.path(f)) for f in files]
            d = json.loads(generate(model, [question + " Answer true only if what you actually perceive confirms it; describe what you see in 'seen'."] + handles,
                                    config={"response_mime_type": "application/json", "response_schema": schema}).text)
            ok, seen = bool(d.get("answer")), str(d.get("seen", ""))[:200]
        except Exception as e:
            ok, seen = False, "perception call failed - " + repr(e)[:140]
        self.results.append(ok)
        print(cid + ": " + ("PASS" if ok else "FAIL") + " - " + claim + " - shown " + shown + " - seen: " + seen)
        return ok

    # ---- the fault-proof: corrupt a COPY every way a lazy or broken artifact could look, and prove the
    # mechanical checks catch each one. v10.3 (one verdict, one truth): deterministic and complete - every
    # fault every run, sites derived from the content instead of random - so the same artifact and the same
    # verify.py always get the same verdict, and a failure names the exact fault no check catches. (v10.2
    # rolled one random fault per run: one artifact passed some runs and failed others for 80 turns.)
    FAULTS = ("blank", "truncate", "placeholder")
    def fault_proof(self, p, mode=None):
        data = self.raw(p)
        if data == b"":
            print("FAULT-PROOF FAILED: " + p + " is missing or empty - nothing to corrupt")
            self.results.append(False)
            return False
        seed = int(hashlib.sha256(data).hexdigest()[:8], 16)   # the content picks the sites - stable per content
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = None
        lo, hi = len(data) // 4, max(len(data) // 2, 1)
        report, failed = [], []
        for m in ([mode] if mode else list(self.FAULTS)):
            if m == "blank":
                bad = b""
            elif m == "truncate":
                bad = data[:lo + seed % max(hi - lo, 1)]
            elif text is None:
                report.append("placeholder: n/a (binary file)")
                continue
            else:
                site = seed % (len(text) + 1)
                bad = (text[:site] + " [PLACEHOLDER - TODO fill this in] " + text[site:]).encode("utf-8")
            copy = os.path.join("scratch", "fault_" + m + "_" + os.path.basename(p))
            open(copy, "wb").write(bad)
            self.override[p] = copy
            caught = [cid for cid, claim, fn in self.checks if not self._run(fn)[0]]
            self.override.pop(p, None)
            report.append(m + ": " + (("caught by " + ", ".join(caught)) if caught else "caught by NOTHING"))
            if not caught:
                failed.append(m)
        if failed == []:
            print("FAULT-PROOF: " + p + " - " + "; ".join(report))
            return True
        hint = {"blank": "kit.min_length(" + repr(p) + ", n)", "truncate": "kit.min_length(" + repr(p) + ", n) or a check on its last part",
                "placeholder": "kit.no_placeholders(" + repr(p) + ")"}
        print("FAULT-PROOF FAILED: " + p + " - " + "; ".join(report) + " - no mechanical check fails a " + " or ".join(failed)
              + " copy of " + p + "; add " + " and ".join(hint[m] for m in failed) + " to a check")
        self.results.append(False)
        return False

    # ---- the last line
    def verdict(self):
        ok = self.results != [] and all(self.results)
        print("VERDICT: " + ("PASS" if ok else "FAIL"))
        sys.exit(0 if ok else 1)
