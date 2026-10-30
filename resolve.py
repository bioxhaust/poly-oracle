"""Check journal markets for resolution; print Brier, log-loss (mine vs market), paper P&L."""
from polyoracle import api, journal, scoring
rows = journal.load(); res = []
for r in rows:
    y = api.resolved_yes(api.market(r["market_id"]))
    if y is None: continue
    s = r.get("paper") or {}
    res.append((r, y, scoring.pnl(s["side"], s["price"], s["stake"], y) if s.get("stake") else 0.0))
print(f"resolved {len(res)}/{len(rows)}")
if res:
    n = len(res)
    for lbl, k in (("mine", "my_prob"), ("market", "market_price")):
        print(lbl, "brier=%.4f logloss=%.4f" % (sum(scoring.brier(r[k], y) for r, y, _ in res)/n, sum(scoring.logloss(r[k], y) for r, y, _ in res)/n))
    print("paper P&L $%.2f" % sum(p for *_, p in res))
