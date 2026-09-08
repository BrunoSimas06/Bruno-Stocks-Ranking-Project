from flask import Flask, jsonify, request
from flask_cors import CORS
from scoring import get_metrics, score_company

app = Flask(__name__)
CORS(app)

NASDAQ_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "AVGO", "PEP",
    "COST", "ADBE", "NFLX", "AMD", "INTC", "CSCO", "CMCSA", "TXN", "QCOM",
    "INTU", "AMGN", "HON", "SBUX", "GILD", "MDLZ", "ADI"
]

NYSE_TICKERS = [
    "JPM", "V", "JNJ", "WMT", "PG", "MA", "HD", "XOM", "CVX", "BAC", "KO",
    "PFE", "DIS", "MRK", "VZ", "T", "WFC", "MCD", "NKE", "ORCL", "CAT",
    "GS", "IBM", "BA", "GE"
]


@app.route("/api/ranking")
def ranking():
    exchange = request.args.get("exchange", "NASDAQ").upper()

    tickers = NASDAQ_TICKERS if exchange == "NASDAQ" else NYSE_TICKERS

    results = []

    for ticker in tickers:
        metrics = get_metrics(ticker)

        if metrics.get("error"):
            continue

        score, details = score_company(metrics)

        results.append({
            "ticker": ticker,
            "score": score,
            **details
        })

    results.sort(key=lambda item: item["score"], reverse=True)

    return jsonify({
        "exchange": exchange,
        "count": len(results),
        "results": results
    })


@app.route("/")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
