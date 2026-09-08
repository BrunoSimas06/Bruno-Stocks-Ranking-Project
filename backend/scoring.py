import yfinance as yf


def get_metrics(ticker):
    """
    Busca os dados financeiros reais da empresa via Yahoo Finance.
    Se algum dado não estiver disponível, retorna None nesse campo,
    sem derrubar o restante do ranking.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
    except Exception:
        return {
            "ticker": ticker,
            "cash": None,
            "total_debt": None,
            "debt_to_equity": None,
            "preferred_equity": None,
            "retained_earnings": None,
            "treasury_shares": None,
            "error": True
        }

    return {
        "ticker": ticker,
        "cash": info.get("totalCash"),
        "total_debt": info.get("totalDebt"),
        "debt_to_equity": info.get("debtToEquity"),
        "preferred_equity": info.get("preferredStockValue"),
        "retained_earnings": info.get("retainedEarnings"),
        "treasury_shares": info.get("sharesOutstanding"),
        "error": False
    }


def score_company(metrics):
    """
    Calcula a pontuação de 0 a 5 com base nos 5 critérios de Buffett.
    Cada critério que não puder ser avaliado (dado ausente) não soma
    ponto, mas também não derruba o cálculo.
    """
    score = 0

    details = {
        "cash_gt_debt": None,
        "debt_to_equity": None,
        "preferred_ok": None,
        "retained_growth_ok": None,
        "treasury_ok": None,
    }

    cash = metrics.get("cash")
    debt = metrics.get("total_debt")

    if cash is not None and debt is not None:
        cash_gt_debt = cash > debt
        details["cash_gt_debt"] = cash_gt_debt
        if cash_gt_debt:
            score += 1

    de_ratio = metrics.get("debt_to_equity")

    if de_ratio is not None:
        de_ratio_normalized = de_ratio / 100 if de_ratio > 10 else de_ratio
        details["debt_to_equity"] = round(de_ratio_normalized, 2)
        if de_ratio_normalized < 0.8:
            score += 1

    preferred = metrics.get("preferred_equity")

    if preferred is not None:
        preferred_ok = preferred == 0
        details["preferred_ok"] = preferred_ok
        if preferred_ok:
            score += 1
    else:
        details["preferred_ok"] = True
        score += 1

    retained = metrics.get("retained_earnings")

    if retained is not None:
        retained_growth_ok = retained > 0
        details["retained_growth_ok"] = retained_growth_ok
        if retained_growth_ok:
            score += 1

    treasury = metrics.get("treasury_shares")

    if treasury is not None:
        details["treasury_ok"] = True
        score += 1

    return score, details
