import json, datetime, pathlib
PATH = pathlib.Path(__file__).resolve().parent.parent / "journal.jsonl"
REQ = ["market_id", "question", "market_price", "my_prob", "sources", "model"]
def add(entry, path=PATH):
    for k in REQ: assert k in entry, k
    assert 0 < entry["my_prob"] < 1 and all(s.get("url") for s in entry["sources"])
    entry = {**entry, "ts_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    with open(path, "a") as f: f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry
def load(path=PATH):
    p = pathlib.Path(path)
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
