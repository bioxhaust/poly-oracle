import json
from polyoracle import scoring, journal
def test_scores():
    assert abs(scoring.brier(0.7, 1) - 0.09) < 1e-12
    assert scoring.logloss(0.5, 0) > 0.69
def test_edge_and_pnl():
    side, px, e = scoring.edge(0.8, 0.6, 0.62, slip=0)
    assert side == "YES" and abs(e - 0.18) < 1e-9
    side, px, e = scoring.edge(0.2, 0.6, 0.62, slip=0)
    assert side == "NO" and abs(px - 0.4) < 1e-9
    assert abs(scoring.pnl("YES", 0.5, 10, 1) - 10) < 1e-9 and scoring.pnl("NO", 0.5, 10, 1) == -10
    assert scoring.kelly_stake(0.4, 0.5, 1000) == 0
def test_journal(tmp_path):
    p = tmp_path / "j.jsonl"
    journal.add({"market_id": "1", "question": "q", "market_price": 0.5, "my_prob": 0.6, "sources": [{"url": "http://x"}], "model": "m"}, p)
    assert journal.load(p)[0]["ts_utc"]
