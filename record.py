"""Record forecasts with live quotes, costs, paper size (bankroll $1000, 1/4 Kelly, cap 5%)."""
from polyoracle import api, journal, scoring
MF="https://midtermforecast.com/data/senate-forecast-2026.csv"; MFH="https://midtermforecast.com/"
CNN="https://edition.cnn.com/2026/10/29/politics/cnn-polls-michigan-maine-texas-kansas-senate-races-midterms-vis"
F = [
 (562802,0.91,[MFH,"https://www.callthemap.com/polls"],"model D House 90%, generic ballot D+6..8"),
 (562794,0.31,[MFH,CNN],"model D Senate 69%"),
 (630964,0.32,[MF,CNN,"https://www.callthemap.com/polls"],"model Paxton 32.7%; YouGov Talarico +8, CNN +6"),
 (630806,0.24,[MF,"https://www.aljazeera.com/news/2026/10/29/us-midterms-five-days-to-go-what-the-polls-say-as-trump-harris-campaign"],"model Rogers 23.2%; Mitchell El-Sayed +7"),
 (634974,0.33,[MF,"https://prod.transcripts.cnn.com/show/cnc/date/2026-10-29/segment/01"],"model Sullivan 35.5%; AK gov probe into Peltola campaign"),
 (5686980,0.62,["https://apnews.com/article/trump-iran-strikes-midterm-elections-c7df622f1e87de6035173be8fb8c4add","https://www.axios.com/2026/10/28/iran-war-arab-mediators-war-post-midterms","https://www.al-monitor.com/originals/2026/10/iran-sees-only-unacceptable-ideas-latest-mediation-end-war-official-says"],"US told allies to prepare for strikes after Nov 3; Iran calls Qatari ideas unacceptable"),
 (5170739,0.12,["https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=30"],"BTC 80.1k, Oct low 79.2k, 30d vol 1.35%/d -> touch-prob ~10% in 2.3d, fat-tail bump"),
]
import sys, json as _j
if len(sys.argv) > 1:  # forecasts file: [[market_id, prob, [urls], note, model], ...]
    F = _j.load(open(sys.argv[1]))
for mid,p,urls,note,*mdl in F:
    m=api.market(mid); bid,ask=api.best_quotes(m)
    side,px,e=scoring.edge(p,bid,ask)
    stake=scoring.kelly_stake(p if side=="YES" else 1-p, px, 1000) if e>0.03 else 0
    journal.add({"market_id":str(mid),"question":m["question"],"url":"https://polymarket.com/market/"+m["slug"],
      "market_price":(bid+ask)/2,"bid":bid,"ask":ask,"my_prob":p,"sources":[{"url":u} for u in urls],"note":note,
      "model":(mdl[0] if mdl else "Grok Bot (manual synthesis; Ollama not used)"),"paper":{"side":side,"price":round(px,4),"edge":round(e,4),"stake":stake}})
    print(f"{mid}|{m['question']}|{bid}/{ask}|{p}|{side} {e:+.3f}|${stake}")
