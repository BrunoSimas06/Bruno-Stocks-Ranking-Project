import yfinance as yf


def get_metrics(ticker):
    try:
        company = yf.Ticker(ticker)
        balance_sheet = company.balance_sheet

        if balance_sheet.empty or balance_sheet.shape[1] < 2:
            return None

        latest = balance_sheet.columns[0]
        previous = balance_sheet.columns[1]

        def get_value(possible_names, column):
            for name in possible_names:
                if name in balance_sheet.index:
                    value = balance_sheet.loc[name, column]

                    if value is not None:
                        try:
                            if value != value:
                                return None
                        except Exception:
                            pass

                        return float(value)

            return None

        return {
            "cash": get_value(
                [
                    "Cash And Cash Equivalents",
                    "Cash Cash Equivalents And Short Term Investments",
                ],
                latest,
            ),
            "debt": get_value(
                [
                    "Total Debt",
                    "Long Term Debt And Capital Lease Obligation",
                ],
                latest,
            ),
            "equity": get_value(
                [
                    "Stockholders Equity",
                    "Common Stock Equity",
                    "Total Equity Gross Minority Interest",
                ],
                latest,
            ),
            "preferred": get_value(
                [
                    "Preferred Stock",
                    "Preferred Shares",
                ],
                latest,
            ),
            "retained_latest": get_value(
                ["Retained Earnings"],
                latest,
            ),
            "retained_previous": get_value(
                ["Retained Earnings"],
                previous,
            ),
            "treasury": get_value(
                [
                    "Treasury Shares Number",
                    "Treasury Stock",
                ],
                latest,
            ),
        }

    except Exception as error:
        print(f"Erro ao buscar {ticker}: {error}")
        return None


def score_company(metrics):
    score = 0
    details = {
        "cash_gt_debt": None,
        "debt_to_equity": None,
        "preferred_ok": None,
        "retained_growth_ok": None,
        "treasury_ok": None,
    }

    cash = metrics.get("cash")
    debt = metrics.get("debt")
    equity = metrics.get("equity")
    preferred = metrics.get("preferred")
    retained_latest = metrics.get("retained_latest")
    retained_previous = metrics.get("retained_previous")
    treasury = metrics.get("treasury")

    # 1. Caixa maior que a dívida
    if cash is not None and debt is not None:
        details["cash_gt_debt"] = cash > debt
        score += int(details["cash_gt_debt"])

    # 2. Dívida sobre patrimônio líquido menor que 0,80
    if debt is not None and equity is not None and equity != 0:
        debt_to_equity = debt / equity
        details["debt_to_equity"] = round(debt_to_equity, 2)

        if debt_to_equity < 0.80:
            score += 1

    # 3. Ausência de ações preferenciais
    # Campo ausente é tratado como zero nesta versão
    if preferred is None or preferred == 0:
        details["preferred_ok"] = True
        score += 1
    else:
        details["preferred_ok"] = False

    # 4. Crescimento dos lucros retidos
    if retained_latest is not None and retained_previous is not None:
        details["retained_growth_ok"] = retained_latest > retained_previous
        score += int(details["retained_growth_ok"])

    # 5. Existência de ações em tesouraria
    if treasury is not None:
        details["treasury_ok"] = treasury != 0
        score += int(details["treasury_ok"])

    return score, details
