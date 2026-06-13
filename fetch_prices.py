#!/usr/bin/env python3
"""Quotes + FX from Yahoo (server-side, no key) -> prices.json. Only tickers, no portfolio data."""
import json, time, urllib.request
SYMBOLS = {
    "VRT": "VRT",
    "PRY": "PRY.MI",
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
    "LEMA": "LEMA.MI",
    "MMM": "MMM",
    "ABBV": "ABBV",
    "ACN": "ACN",
    "ACOMO": "ACOMO",
    "ADBE": "ADBE",
    "AD": "AD",
    "ABNB": "ABNB",
    "BABA": "BABA",
    "AMD": "AMD",
    "AASI": "AASI",
    "AAPL": "AAPL",
    "APP": "APP",
    "ADM": "ADM",
    "ARM": "ARM",
    "ASML": "ASML",
    "1ASML": "1ASML",
    "B": "B",
    "BRK.B": "BRK.B",
    "BLCO": "BLCO",
    "BHP": "BHP",
    "RX": "RX",
    "BA": "BA",
    "BKNG": "BKNG",
    "AVGO": "AVGO",
    "BAM": "BAM",
    "BN": "BN",
    "BC": "BC",
    "BZZUY": "BZZUY",
    "BYDDY": "BYDDY",
    "CPR": "CPR",
    "CAP": "CAP",
    "CPRI": "CPRI",
    "1afx": "1afx",
    "CAVA": "CAVA",
    "CELH": "CELH",
    "0001": "0001",
    "CLSK": "CLSK",
    "NET": "NET",
    "KO": "KO",
    "CL": "CL",
    "CFRUY": "CFRUY",
    "CSU": "CSU",
    "CPRT": "CPRT",
    "CRWV": "CRWV",
    "CPNG": "CPNG",
    "CROX": "CROX",
    "CRWD": "CRWD",
    "DJCO": "DJCO",
    "QTUM": "QTUM",
    "DEO": "DEO",
    "DLO": "DLO",
    "DUOL": "DUOL",
    "EDEN": "EDEN",
    "ESL": "ESL",
    "SX5E": "SX5E",
    "ERFSF": "ERFSF",
    "FIh.u": "FIh.u",
    "FMX": "FMX",
    "RACE": "RACE",
    "FBK": "FBK",
    "FVRR": "FVRR",
    "O3I": "O3I",
    "FMC": "FMC",
    "FTNT": "FTNT",
    "GRAB": "GRAB",
    "HIMS": "HIMS",
    "IDEXY": "IDEXY",
    "INFY": "INFY",
    "INTC": "INTC",
    "IWB": "IWB",
    "JDSPY": "JDSPY",
    "JD": "JD",
    "JEDI": "JEDI",
    "JNJ": "JNJ",
    "JMIA": "JMIA",
    "K": "K",
    "KER": "KER",
    "2222.0": "2222.0",
    "KWEB": "KWEB",
    "LMND": "LMND",
    "LDO": "LDO",
    "LVMHF": "LVMHF",
    "MOH": "MOH",
    "LYFT": "LYFT",
    "AMKBY": "AMKBY",
    "MKL": "MKL",
    "MAR": "MAR",
    "MASI": "MASI",
    "MCD": "MCD",
    "Meli": "Meli",
    "MONC": "MONC",
    "MNDY": "MNDY",
    "NDX": "NDX",
    "NESN": "NESN",
    "NEM": "NEM",
    "NEXI": "NEXI",
    "NTDOY": "NTDOY",
    "NVO": "NVO",
    "NTNX": "NTNX",
    "NVR": "NVR",
    "OKLO": "OKLO",
    "OKTA": "OKTA",
    "ORCL": "ORCL",
    "ORSTED": "ORSTED",
    "OSCR": "OSCR",
    "PLTR": "PLTR",
    "2PP": "2PP",
    "PEP": "PEP",
    "PSH": "PSH",
    "PFE": "PFE",
    "PQ": "PQ",
    "PG": "PG",
    "PRX": "PRX",
    "PUBM": "PUBM",
    "RL": "RL",
    "RELY": "RELY",
    "REY.MI": "REY.MI",
    "RIO": "RIO",
    "RKLB": "RKLB",
    "RBSFY": "RBSFY",
    "RYAAY": "RYAAY",
    "VOO": "VOO",
    ".INX": ".INX",
    "CRM": "CRM",
    "IOT": "IOT",
    "SMTI": "SMTI",
    "SAP": "SAP",
    "SES": "SES",
    "SMH": "SMH",
    "NOW": "NOW",
    "SHOP": "SHOP",
    "SIE": "SIE",
    "SNOW": "SNOW",
    "SBUX": "SBUX",
    "STLAM": "STLAM",
    "STNE": "STNE",
    "SG": "SG",
    "TROW": "TROW",
    "TSM": "TSM",
    "TPR": "TPR",
    "TGT": "TGT",
    "TDOC": "TDOC",
    "TCEHY": "TCEHY",
    "TSLA": "TSLA",
    "HEAL": "HEAL",
    "TTD": "TTD",
    "PATH": "PATH",
    "ULTA": "ULTA",
    "UA": "UA",
    "UNH": "UNH",
    "GDX": "GDX",
    "QNTM": "QNTM",
    "VUAA": "VUAA",
    "VEEV": "VEEV",
    "V": "V",
    "VISA": "VISA",
    "VST": "VST",
    "VOW3": "VOW3",
    "WBD": "WBD",
    "WM": "WM",
    "XOVR": "XOVR",
    "ZM": "ZM",
    "IFX": "IFX.DE",
    "SAN": "SAN.PA",
    "ALV": "ALV.DE",
    "HDB": "HDB",
    "SU": "SU.PA",
    "RHM": "RHM.DE",
    "AEM": "AEM",
    "8058.T": "8058.T",
    "AZN": "AZN",
    "CCJ": "CCJ",
    "AXA": "CS.PA",
    "TLX": "TLX.DE",
    "MRK.DE": "MRK.DE",
    "RDY": "RDY",
    "BAP": "BAP",
    "EURUSD": "EURUSD=X",
    "EURJPY": "EURJPY=X",
    "EURCAD": "EURCAD=X",
    "EURGBP": "EURGBP=X",
    "EURCHF": "EURCHF=X",
    "EURSEK": "EURSEK=X",
    "APLD": "APLD",
    "IREN": "IREN",
    "MRVL": "MRVL",
    "MU": "MU",
    "SOFI": "SOFI",
    "STM": "STM",
    "REC": "REC.MI",
    "MUV2": "MUV2.DE",
    "IBN": "IBN",
    "IBE": "IBE.MC",
    "GEV": "GEV"
}
INDICES = {
    "IDX_SPX": "%5EGSPC",
    "IDX_NDX": "%5ENDX",
    "IDX_HSI": "%5EHSI",
    "IDX_NIFTY": "%5ENSEI",
    "IDX_BTC": "BTC-USD",
}
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
           "Accept": "application/json,text/plain,*/*"}
HOSTS = ["https://query1.finance.yahoo.com", "https://query2.finance.yahoo.com"]

# Shared session WITH a cookie. Yahoo rejects the first cookie-less requests with
# 401, which used to silently kill the first few symbols (VRT, PRY, META...).
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
for _ in range(2):
    try:
        opener.open(urllib.request.Request("https://finance.yahoo.com",
                    headers=HEADERS), timeout=15).read(1); break
    except Exception:
        time.sleep(1)

def _fetch(ysym, host):
    url = f"{host}/v8/finance/chart/{ysym}?interval=1d&range=1d"
    with opener.open(urllib.request.Request(url, headers=HEADERS), timeout=15) as r:
        m = json.load(r)["chart"]["result"][0]["meta"]
    p = m.get("regularMarketPrice"); pc = m.get("chartPreviousClose") or m.get("previousClose")
    if not p or not pc: raise ValueError("no price")
    return {"p": round(p, 4), "d": round((p/pc-1)*100, 2)}

def quote(ysym):
    last = None
    for attempt in range(3):                       # retry across both Yahoo hosts
        try:
            return _fetch(ysym, HOSTS[attempt % len(HOSTS)])
        except Exception as e:
            last = e; time.sleep(0.6 * (attempt + 1))
    raise last

def _fetch_idx(ysym, host):
    url = f"{host}/v8/finance/chart/{ysym}?interval=1d&range=1y"
    with opener.open(urllib.request.Request(url, headers=HEADERS), timeout=20) as r:
        res = json.load(r)["chart"]["result"][0]
    m = res["meta"]
    p = m.get("regularMarketPrice"); pc = m.get("chartPreviousClose") or m.get("previousClose")
    closes = [c for c in (res.get("indicators", {}).get("quote", [{}])[0].get("close") or []) if c]
    top = max(closes + ([p] if p else []))
    if not p or not pc or not top: raise ValueError("no idx data")
    return {"p": round(p, 4), "d": round((p/pc-1)*100, 2), "t": round(top, 4)}

def quote_idx(ysym):
    last = None
    for attempt in range(3):
        try:
            return _fetch_idx(ysym, HOSTS[attempt % len(HOSTS)])
        except Exception as e:
            last = e; time.sleep(0.6 * (attempt + 1))
    raise last

# Carry forward the previous good value if a symbol fails -> it never drops to a stale book price.
try: prev = json.load(open("prices.json"))
except Exception: prev = {}

out = {}; fail = []
for ticker, ysym in INDICES.items():
    try:
        out[ticker] = quote_idx(ysym)
    except Exception:
        fail.append(ticker)
        if isinstance(prev.get(ticker), dict): out[ticker] = prev[ticker]
    time.sleep(0.3)
for ticker, ysym in SYMBOLS.items():
    try:
        out[ticker] = quote(ysym)
    except Exception:
        fail.append(ticker)
        if isinstance(prev.get(ticker), dict): out[ticker] = prev[ticker]
    time.sleep(0.3)

out["_updated"] = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
json.dump(out, open("prices.json", "w"), indent=0)
print(f"wrote prices.json: {len(out)-1} symbols, {len(fail)} failed -> {fail[:25]}")
