def get_metrics(ticker):
    """
    Modo de demonstração.
    Não consulta mais o yfinance, evitando a queda do Render.
    """
    valores = {
        "AAPL": 5,
        "MSFT": 5,
        "GOOGL": 4,
        "AMZN": 4,
        "NVDA": 4,
        "META": 4,
        "TSLA": 3,
        "AVGO": 4,
        "PEP": 3,
        "COST": 4,
        "ADBE": 4,
        "NFLX": 3,
        "AMD": 3,
        "INTC": 2,
        "CSCO": 4,
        "CMCSA": 2,
        "TXN": 4,
        "QCOM": 3,
        "INTU": 4,
        "AMGN": 3,
        "HON": 4,
        "SBUX": 3,
        "GILD": 3,
        "MDLZ": 3,
        "ADI": 4,

        "JPM": 4,
        "V": 5,
        "JNJ": 4,
        "WMT": 4,
        "PG": 4,
        "MA": 5,
        "HD": 4,
        "XOM": 4,
        "CVX": 3,
        "BAC": 3,
        "KO": 4,
        "PFE": 2,
        "DIS": 2,
        "MRK": 4,
        "VZ": 2,
        "T": 2,
        "WFC": 3,
        "MCD": 4,
        "NKE": 3,
        "ORCL": 4,
        "CAT": 4,
        "GS": 4,
        "IBM": 3,
        "BA": 2,
        "GE": 4
    }

    score = valores.get(ticker, 3)

    return {
        "ticker": ticker,
        "demo_score": score
    }


def score_company(metrics):
    score = metrics.get("demo_score", 3)

    details = {
        "cash_gt_debt": score >= 3,
        "debt_to_equity": round(max(0.25, 1.1 - score * 0.15), 2),
        "preferred_ok": score >= 3,
        "retained_growth_ok": score >= 3,
        "treasury_ok": score >= 3,
    }

    return score, details
