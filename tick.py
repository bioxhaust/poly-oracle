"""Periodic tick: snapshot bid/ask of open journal markets -> logs/quotes.jsonl; run resolve.py -> logs/resolve.log."""
import json, datetime, pathlib, subprocess, sys
from polyoracle import api, journal
ROOT = pathlib.Path(__file__).resolve().parent; LOGS = ROOT / "logs"; LOGS.mkdir(exist_ok=True)
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
ids = sorted({r["market_id"] for r in journal.load()})
with open(LOGS / "quotes.jsonl", "a") as f:
    for mid in ids:
        try:
            m = api.market(mid)
            if m.get("closed"): continue
            bid, ask = api.best_quotes(m)
            f.write(json.dumps({"ts_utc": now(), "market_id": mid, "bid": bid, "ask": ask}) + "\n")
        except Exception as e:
            f.write(json.dumps({"ts_utc": now(), "market_id": mid, "error": str(e)[:200]}) + "\n")
out = subprocess.run([sys.executable, str(ROOT / "resolve.py")], cwd=ROOT, capture_output=True, text=True)
with open(LOGS / "resolve.log", "a") as f:
    for line in (out.stdout + out.stderr).splitlines(): f.write(f"[{now()}] {line}\n")
sys.exit(out.returncode)
