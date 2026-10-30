import math
FEE = 0.0  # Polymarket taker fee on most markets; set per market if nonzero
SLIP = 0.005
def brier(p, y): return (p - y) ** 2
def logloss(p, y, eps=1e-6):
    p = min(max(p, eps), 1 - eps); return -(y * math.log(p) + (1 - y) * math.log(1 - p))
def edge(p, bid, ask, fee=FEE, slip=SLIP):
    """Net edge per $1 share after crossing spread + slippage + fee. Returns (side, entry_price, edge)."""
    buy_yes = ask + slip + fee; buy_no = (1 - bid) + slip + fee
    ey, en = p - buy_yes, (1 - p) - buy_no
    return ("YES", buy_yes, ey) if ey >= en else ("NO", buy_no, en)
def kelly_stake(prob_win, price, bankroll, frac=0.25, cap=0.05):
    if price >= 1 or prob_win <= price: return 0.0
    f = (prob_win - price) / (1 - price)
    return round(min(f * frac, cap) * bankroll, 2)
def pnl(side, price, stake, y):
    shares = stake / price; win = (y == 1) if side == "YES" else (y == 0)
    return shares * (1 if win else 0) - stake
