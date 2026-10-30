"""Public Polymarket API client (read-only)."""
import json, urllib.request, urllib.parse
GAMMA = "https://gamma-api.polymarket.com"; CLOB = "https://clob.polymarket.com"
def _get(url, params=None):
    if params: url += "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "polyoracle"}), timeout=20) as r:
        return json.load(r)
def market(mid): return _get(f"{GAMMA}/markets/{mid}")
def markets(**p): return _get(f"{GAMMA}/markets", p)
def yes_token(m): return json.loads(m["clobTokenIds"])[0]
def book(token): return _get(f"{CLOB}/book", {"token_id": token})
def best_quotes(m):
    b = book(yes_token(m))
    bid = max((float(x["price"]) for x in b.get("bids", [])), default=None)
    ask = min((float(x["price"]) for x in b.get("asks", [])), default=None)
    return bid, ask
def resolved_yes(m):
    """Return 1/0 if market closed and resolved, else None."""
    if not m.get("closed"): return None
    p = [float(x) for x in json.loads(m["outcomePrices"])]
    return 1 if p[0] > 0.99 else 0 if p[0] < 0.01 else None
