#!/usr/bin/env python3
"""Fetches live quotes from Yahoo Finance (server-side, no key needed) and writes prices.json.
Run automatically by GitHub Actions. Contains ONLY ticker symbols - no portfolio data."""
import json, time, urllib.request

# dashboard ticker -> Yahoo symbol
SYMBOLS = {
    "META": "META",
    "GOOGL": "GOOGL",
    "NFLX": "NFLX",
    "AMZN": "AMZN",
    "MSFT": "MSFT",
    "NVDA": "NVDA",
    "NBIS": "NBIS",
    "MELI": "MELI",
    "SE": "SE",
    "UBER": "UBER",
    "AXON": "AXON",
    "IT": "IT",
    "LULU": "LULU",
    "DECK": "DECK",
    "ONON": "ONON",
    "NKE": "NKE",
    "DIS": "DIS",
    "PYPL": "PYPL",
    "FOUR": "FOUR",
    "XYZ": "XYZ",
    "BRK/B": "BRK-B",
    "LVMH": "MC.PA",
    "ADYEN": "ADYEN.AS",
    "FFH": "FFH.TO",
    "HTHIY": "6501.T",
    "XEON": "XEON.DE",
    "ISAC": "ISAC.L",
    "XDWH": "XDWH.DE",
    "URNU": "URNU.L",
    "FLXI": "FLXI.DE",
    "ABT": "ABT",
    "CMG": "CMG",
    "ISRG": "ISRG",
    "STZ": "STZ",
    "TMDX": "TMDX",
    "NU": "NU",
    "PDD": "PDD",
    "LEU": "LEU",
    "ALC": "ALC",
    "ABF": "ABF.L",
    "HEIA": "HEIA.AS",
    "NMAN": "NMAN.ST",
    "HESAY": "HESAY",
    "PDRDF": "PDRDF",
    "ESIS": "ESIS.DE",
    "DAPP": "DAPP.L",
    "CI2": "FLXI.DE",
    "CPH": "CPH.TO",
    "CSBGE7": "CSBGE7.MI",
    "LEMA": "LEMA.MI"
}

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; price-bot/1.0)"}

def quote(ysym):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ysym}?interval=1d&range=1d"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        j = json.load(r)
    m = j["chart"]["result"][0]["meta"]
    p = m.get("regularMarketPrice")
    pc = m.get("chartPreviousClose") or m.get("previousClose")
    if not p or not pc:
        raise ValueError("no price")
    return {"p": round(p, 4), "d": round((p/pc - 1)*100, 2)}

out = {}
for ticker, ysym in SYMBOLS.items():
    try:
        out[ticker] = quote(ysym)
    except Exception as e:
        print(f"skip {ticker} ({ysym}): {e}")
    time.sleep(0.3)  # be gentle

out["_updated"] = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
with open("prices.json", "w") as f:
    json.dump(out, f, indent=0)
print(f"wrote prices.json with {len(out)-1} quotes")
