import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from scoring import get_metrics, score_company
from tickers import EXCHANGES


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "API do Ranking de Ações está funcionando"
    })


@app.route("/api/ranking")
def ranking():
    exchange = request.args.get("exchange", "NASDAQ").upper()

    if exchange not in EXCHANGES:
        return jsonify({
            "error": "Bolsa inválida. Use NASDAQ ou NYSE."
        }), 400

    tickers = EXCHANGES[exchange]
    results = []

    for ticker in tickers:
        print(f"Buscando dados de {ticker}...")

        metrics = get_metrics(ticker)

        if metrics is None:
            print(f"Dados insuficientes para {ticker}")
            continue

        score, details = score_company(metrics)

        results.append({
            "ticker": ticker,
            "score": score,
            **details
        })

    # Ordena pela maior pontuação.
    # Em caso de empate, prioriza menor dívida/patrimônio.
    results.sort(
        key=lambda item: (
            item["score"],
            -(item["debt_to_equity"] or 999)
        ),
        reverse=True
    )

    return jsonify({
        "exchange": exchange,
        "count": len(results),
        "results": results[:25]
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
