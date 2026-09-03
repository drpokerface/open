# metered.py - VALIDATED: the money meter; every model/media call routes here and logs rupees to spend.jsonl
import os, json, time, logging
from google import genai
logging.getLogger("google_genai").setLevel(logging.ERROR)   # v10.1: silence the AFC warning (noise, not an error)
_client = None
def client():
    # the one lazy real client; prefer generate()/generate_media()/upload() below over raw calls
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client
# rupees per 1M tokens (input, output) - EDIT to match your real billing; unknown models use DEFAULT
PRICES = {"gemini-3.5-flash": (8.0, 33.0), "gemini-3.1-pro-preview": (105.0, 840.0), "DEFAULT": (105.0, 840.0)}
# v8.3 MODEL ALIASES: names agents habitually write that are NOT on this key are rerouted to the
# verified equivalent, so a dead judge model can never sink a gate (gemini-3.5-pro is 404 NOT_FOUND
# on this key - one run failed C4 on it every time). EDIT to match your key; see providers.md.
ALIASES = {"gemini-3.5-pro": "gemini-3.1-pro-preview"}
_aliased = set()
def _attested():
    # v9 (design 2): capabilities.json (written by `python swarm.py probe`) is the machine-verified
    # truth about this key; a model it records as dead is rerouted to a live one of the same tier
    try:
        led = json.load(open("capabilities.json", encoding="utf-8"))
        return {k: v.get("ok", False) for k, v in led.get("models", {}).items()}
    except Exception:
        return {}
# rupees per generated unit - EDIT to your billing (used by generate_media)
FLAT = {"image": 3.5, "audio_second": 0.2, "video_second": 4.0}
def log_spend(kind, model, rupees, note=""):
    with open("spend.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": time.time(), "kind": kind, "model": model, "inr": round(float(rupees), 4), "note": str(note)[:120]}) + "\n")
def spend_total(path="spend.jsonl"):
    total = 0.0
    if os.path.exists(path):
        for line in open(path, encoding="utf-8", errors="ignore"):
            try:
                total += float(json.loads(line).get("inr", 0))
            except Exception:
                pass
    return round(total, 2)
def generate(model, contents, config=None):
    # metered text/JSON call: cost computed from real token usage
    if model in ALIASES:   # v8.3: reroute a dead model name (announced once per process)
        if model not in _aliased:
            _aliased.add(model)
            print("metered: " + model + " is not on this key - routed to " + ALIASES[model])
        model = ALIASES[model]
    known = _attested()
    if known and known.get(model) is False:   # v9: the ledger says this name is dead on this key
        live = [k for k, ok in known.items() if ok]
        pick = next((k for k in live if ("pro" in k) == ("pro" in model)), live[0] if live else model)
        if model not in _aliased:
            _aliased.add(model)
            print("metered: " + model + " is recorded as unreachable on this key (capabilities.json) - routed to " + pick)
        model = pick
    reply = client().models.generate_content(model=model, contents=contents, **({"config": config} if config else {}))
    u = reply.usage_metadata
    pin, pout = PRICES.get(model, PRICES["DEFAULT"])
    if u is not None:
        prompt_toks = u.prompt_token_count or 0
        out_toks = max((u.total_token_count or 0) - prompt_toks, 0)
        cost = (prompt_toks * pin + out_toks * pout) / 1e6
    else:
        cost = 0.05
    log_spend("llm", model, cost)
    return reply
def generate_media(kind, units, make, model="?", note=""):
    # metered media call: state kind ('image'|'audio_second'|'video_second') and units, pass the real call as make()
    out = make()
    log_spend(kind, model, FLAT.get(kind, 1.0) * float(units), note)
    return out
def upload(file):
    return client().files.upload(file=file)
