#!/usr/bin/env python3
"""Quotes + FX from Yahoo (server-side, no key) -> prices.json. Only tickers, no portfolio data.

READY TO COMMIT to lellidavide87/stock-prices - prepared 31 Aug 2026.

The GitHub Action runs the REPO copy of this file, not the local one, so local fixes never reach
the dashboard. The repo copy is missing 14 symbols outright and carries 24 BARE tickers that
silently resolve to a US namesake or to nothing - which is why 55 board rows never update and 25
of those sit in ACT and BEST OPPORTUNITY with a frozen price, including the NESTLE, SIEMENS and
ESSILORLUXOTTICA holdings.

ADDED (14): 005380, 8058, 8766, AKRBP, BMY, ENR, GLOB, KWBE, MBG.DE, MOS, NTR, NXPI, TPW, WBD.MI
SUFFIXED (24): NESN->NESN.SW, SIE->SIE.DE, ESL->EL.PA, LDO->LDO.MI, PQ->PQ.MI, PRX->PRX.AS,
  KER->KER.PA, MONC->MONC.MI, CPR->CPR.MI, NEXI->NEXI.MI, CAP->CAP.PA, 0001->0001.HK, RX->RX.V,
  SES->SES.TO, IWB->IWB.MI, ORSTED->ORSTED.CO, STLAM->STLAM.MI, VOW3->VOW3.DE, VUAA->VUAA.MI,
  1afx->AFX.DE, ACOMO->ACOMO.AS, CSU->CSU.TO, VISA->V, 2222.0->2222.T
UNMAPPED rather than guessed: EDEN, CI2, QNTM, FBK - each returned a price 0.04x-4.9x the stored
  one, so the ticker is the wrong instrument and needs identifying first.
"""
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
    "6501.T": "6501.T",
    "XEON": "XEON.DE",
    "ISAC": "ISAC.MI",
    "XDWH": "XDWH.DE",
    "URNU": "URNU.MI",
    "KWBE": "KWBE.MI",
    "005380": "005380.KS", "005385": "005385.KS", "SNPS": "SNPS", "COHR": "COHR",
    # ADDED 21 Aug 2026 - board tickers that had NO live price. Every non-US line carries its
    # SUFFIX: a bare ticker silently resolves to a US namesake or to nothing at all, which is exactly
    # how ACOMO/CSU/VISA came to sit in this map with no price for weeks (fixed in the same pass:
    # ACOMO->ACOMO.AS, CSU->CSU.TO, VISA->V). All eleven were verified against Yahoo before adding -
    # correct instrument name AND a sane ratio to the baked price.
    "8766": "8766.T", "KSPI": "KSPI", "LBTYA": "LBTYA", "MDLZ": "MDLZ",
    "NXPI": "NXPI", "SPCX": "SPCX", "XOM": "XOM", "YSN": "YSN.DE",
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
    "DAPP": "DAPP.MI",
    # "CI2": UNMAPPED 31 Aug 2026. Mapped to FLXI.DE, which returns 35.80 against a board price of 911
#   - 0.04x. Wrong instrument.
    "CPH": "CPH.TO",
    "CSBGE7": "CSBGE7.MI",
    "LEMA": "LEMA.MI",
    "SJPA": "SJPA.MI",
    "CRUD": "CRUD.MI",
    "XGDU": "XGDU.MI",
    "MMM": "MMM",
    "ABBV": "ABBV",
    "ACN": "ACN",
    "ACOMO": "ACOMO.AS",
    "ADBE": "ADBE",
    "AD": "AD",
    "ABNB": "ABNB",
    "BABA": "BABA",
    "AMD": "AMD",
    "AASI": "AASI.MI",  # Amundi Index Solutions ETF, Milan - 0.95x stored
    "AAPL": "AAPL",
    "APP": "APP",
    "ADM": "ADM",
    "ARM": "ARM",
    "ASML": "ASML",
    "1ASML": "1ASML.MI",  # ASML on the Borsa Italiana Global Equity Market, the "1" prefix - 1.00x stored
    "B": "B",
    "BLCO": "BLCO",
    "BHP": "BHP",
    "RX": "RX.V",
    "BA": "BA",
    "BKNG": "BKNG",
    "AVGO": "AVGO",
    "BAM": "BAM",
    "BN": "BN",
    "BC": "BC",
    "BZZUY": "BZZUY",
    "BYDDY": "BYDDY",
    "CPR": "CPR.MI",
    "CAP": "CAP.PA",
    "CPRI": "CPRI",
    "1afx": "AFX.DE",
    "CAVA": "CAVA",
    "CELH": "CELH",
    "0001": "0001.HK",
    "CLSK": "CLSK",
    "NET": "NET",
    "KO": "KO",
    "CL": "CL",
    "CFRUY": "CFRUY",
    "CSU": "CSU.TO",
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
    # "EDEN": UNMAPPED 31 Aug 2026. The bare ticker returns a US ETF at 117.33 against a board price of
#   23.97 - 4.9x, so it is the wrong instrument. Left out rather than guessed.
    "ESL": "EL.PA",
    "SX5E": "^STOXX50E",  # EURO STOXX 50 index - 1.05x stored
    "ERFSF": "ERFSF",
    "FIh.u": "FIH-U.TO",  # Fairfax India Holdings, Toronto USD unit - 1.01x stored
    "FMX": "FMX",
    "RACE": "RACE",
    # "FBK": UNMAPPED 31 Aug 2026. FBK.MI is FinecoBank at about EUR 23.72 against a board price of
#   61.34 - 0.39x, so the board row is NOT FinecoBank. Needs identifying before it is mapped.
    "FVRR": "FVRR",
    "FMC": "FMC",
    "FTNT": "FTNT",
    "GRAB": "GRAB",
    "HIMS": "HIMS",
    "IDEXY": "IDEXY",
    "INFY": "INFY",
    "INTC": "INTC",
    "IWB": "IWB.MI",
    "JDSPY": "JDSPY",
    "JD": "JD",
    "JEDI": "JEDI",
    "JNJ": "JNJ",
    "JMIA": "JMIA",
    "K": "K.TO",  # Kinross Gold, Toronto - 1.08x stored
    "KER": "KER.PA",
    "2222.0": "2222.T",     # KOTOBUKI, Tokyo. I mapped this to 2222.SR (Saudi Aramco) on 31 Aug and
                        # the ratio check caught it instantly - Aramco quotes near SAR 26 against a
                        # board price of 2,159. Wrong company, right-looking ticker.
    "LMND": "LMND",
    "LDO": "LDO.MI",
    "LVMHF": "LVMHF",
    "MOH": "MOH",
    "LYFT": "LYFT",
    "AMKBY": "AMKBY",
    "MKL": "MKL",
    "MAR": "MAR",
    "MASI": "MASI.MI",  # Masi Agricola SpA, Milan - 0.87x stored, accepted on an exact name match
    "MCD": "MCD",
    "Meli": "Meli",
    "MONC": "MONC.MI",
    "MNDY": "MNDY",
    "NDX": "^NDX",
    "NESN": "NESN.SW",
    "NEM": "NEM",
    "NEXI": "NEXI.MI",
    "NTDOY": "NTDOY",
    "NVO": "NVO",
    "NTNX": "NTNX",
    "NVR": "NVR",
    "OKLO": "OKLO",
    "OKTA": "OKTA",
    "ORCL": "ORCL",
    "ORSTED": "ORSTED.CO",
    "OSCR": "OSCR",
    "PLTR": "PLTR",
    "PEP": "PEP",
    "PSH": "PSH",
    "PFE": "PFE",
    "PQ": "PQ.MI",
    "PG": "PG",
    "PRX": "PRX.AS",
    "PUBM": "PUBM",
    "RL": "RL",
    "RELY": "RELY",
    "REY.MI": "REY.MI",
    "RIO": "RIO",
    "RKLB": "RKLB",
    "RBSFY": "RBSFY",
    "RYAAY": "RYAAY",
    "VOO": "VOO",
    ".INX": "^GSPC",  # S&P 500 index - 1.02x stored
    "CRM": "CRM",
    "IOT": "IOT",
    "SMTI": "SMTI",
    "SAP": "SAP",
    "SES": "SES.TO",
    "SMH": "SMH",
    "NOW": "NOW",
    "SHOP": "SHOP",
    "SIE": "SIE.DE",
    "SNOW": "SNOW",
    "SBUX": "SBUX",
    "STLAM": "STLAM.MI",
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
    # "QNTM": UNMAPPED 31 Aug 2026. Returns 3.17 against a board price of 29.35 - 0.11x.
    "VUAA": "VUAA.MI",
    "VEEV": "VEEV",
    "V": "V",
    "VISA": "V",
    "VST": "VST",
    "VOW3": "VOW3.DE",
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
    "GEV": "GEV",
    # --- added 17 Aug 2026. EVERY ONE resolved live against the board's stored price before
    # committing: a bare ticker grabs the US namesake. FLOW bare = a USD NYSEArca ETF at $43.21
    # (real: FLOW.AS, EUR27.64 Amsterdam). CNQ bare = the NYSE USD line at $49.27 against a
    # C$55.17 level, which would have rendered a FALSE HIT — CNQ.TO is C$68.38 Toronto.
    "FLOW": "FLOW.AS",
    "LIN": "LIN",
    "FNV": "FNV",
    "CNQ": "CNQ.TO",
    "HHH": "HHH",
    "INTU": "INTU",
    "SPGI": "SPGI",
    "ROP": "ROP",
    "MCO": "MCO",
    # ===== ADDED 31 Aug 2026 - TEN GRADED NAMES THAT COULD NEVER REFRESH =====
    # Each of these carried a quality score AND an intrinsic value while having no entry here at all,
    # so its board price was frozen at whatever was last baked in. Aker BP was 18% stale and Moncler
    # 15%, both sitting within a few points of clearing their gate - the distance to a buy level is
    # only as good as the price under it. Every non-US line carries its SUFFIX, per the 21 Aug lesson:
    # a bare ticker silently resolves to a US namesake or to nothing.
    "8058": "8058.T",        # Mitsubishi Corp, Tokyo
    "AKRBP": "AKRBP.OL",     # Aker BP, Oslo
    "BMY": "BMY",
    "ENR": "ENR.DE",         # SIEMENS ENERGY - the bare ENR is ENERGIZER in the US, the collision
                             # that put Energizer's dividend on this row in the August sweep.
    "GLOB": "GLOB",
    "MBG.DE": "MBG.DE",      # Mercedes-Benz
    "MOS": "MOS",
    "NTR": "NTR",
    "TPW": "TPW.AX",         # Temple & Webster, ASX - added to the board 31 Aug and never mapped
    "WBD.MI": "WBD.MI",      # WEBUILD, Milan. NOT Warner Bros Discovery, which is WBD in the US.
}
INDICES = {
    "IDX_SPX": "%5EGSPC",
    "IDX_NDX": "%5ENDX",
    "IDX_HSI": "%5EHSI",
    "IDX_NIFTY": "%5ENSEI",
    "IDX_BTC": "BTC-USD",
    "IDX_SMH": "SMH",
    "IDX_LEMA": "LEMA.MI",
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
    p = m.get("regularMarketPrice")
    closes = [c for c in (res.get("indicators", {}).get("quote", [{}])[0].get("close") or []) if c]
    top = max(closes + ([p] if p else []))
    # chartPreviousClose on a 1y-range chart is the close from ~1yr ago, NOT yesterday's
    # close -> using it for the daily % gives nonsense (e.g. "+23%" days). Derive the
    # real previous close from the daily closes series instead.
    # Note: p is rounded to 4dp but closes[] are raw floats, so compare rounded values
    # (a raw tolerance of 1e-6 was too tight and never matched, e.g. 7431.4599609375
    # vs 7431.46 -> diff ~4e-5 -> always fell into the "else" branch, giving d≈0).
    pc = None
    if len(closes) >= 2:
        pc = closes[-2] if (p and abs(round(closes[-1], 4) - p) < 1e-6) else closes[-1]
    if pc is None:
        pc = m.get("chartPreviousClose") or m.get("previousClose")
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
for ticker, ysym in SYMBOLS.items():
    try:
        out[ticker] = quote(ysym)
    except Exception:
        if ticker in prev:
            out[ticker] = prev[ticker]
        fail.append(ticker)

for ticker, ysym in INDICES.items():
    try:
        out[ticker] = quote_idx(ysym)
    except Exception:
        if ticker in prev:
            out[ticker] = prev[ticker]
        fail.append(ticker)

out["_updated"] = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
with open("prices.json", "w", encoding="utf-8") as fh:      # UTF-8, no BOM
    json.dump(out, fh, ensure_ascii=False)

print("wrote prices.json: %d ok, %d carried/failed (%s)" % (
    len(out) - len(fail) - 1, len(fail), ", ".join(fail) if fail else "none"))