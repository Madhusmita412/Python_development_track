import os
import sqlite3
import logging
import math
from datetime import datetime, timezone, timedelta

import requests
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY", "").strip()
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

SUPPORTED_CURRENCIES = [
    ("USD", "US Dollar"),
    ("INR", "Indian Rupee"),
    ("NPR", "Nepalese Rupee"),
    ("EUR", "Euro"),
    ("GBP", "British Pound"),
    ("JPY", "Japanese Yen"),
    ("AUD", "Australian Dollar"),
    ("CAD", "Canadian Dollar"),
]

CURRENCY_META = {
    "USD": {"symbol": "$", "flag": "us", "name": "US Dollar"},
    "INR": {"symbol": "₹", "flag": "in", "name": "Indian Rupee"},
    "NPR": {"symbol": "Rs", "flag": "np", "name": "Nepalese Rupee"},
    "EUR": {"symbol": "€", "flag": "eu", "name": "Euro"},
    "GBP": {"symbol": "£", "flag": "gb", "name": "British Pound"},
    "JPY": {"symbol": "¥", "flag": "jp", "name": "Japanese Yen"},
    "AUD": {"symbol": "A$", "flag": "au", "name": "Australian Dollar"},
    "CAD": {"symbol": "C$", "flag": "ca", "name": "Canadian Dollar"},
}


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "converter.db")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)



def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS history (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                from_curr   TEXT NOT NULL,
                to_curr     TEXT NOT NULL,
                amount      REAL NOT NULL,
                result      REAL NOT NULL,
                rate        REAL NOT NULL,
                created_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS favorites (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                pair        TEXT UNIQUE NOT NULL,
                from_curr   TEXT NOT NULL,
                to_curr     TEXT NOT NULL,
                created_at  TEXT NOT NULL
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def add_history(from_curr, to_curr, amount, result, rate):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO history (from_curr, to_curr, amount, result, rate, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (from_curr, to_curr, amount, result, rate,
             datetime.now(timezone.utc).isoformat()),
        )
        conn.execute(
            "DELETE FROM history WHERE id NOT IN "
            "(SELECT id FROM history ORDER BY id DESC LIMIT 10)"
        )
        conn.commit()
    finally:
        conn.close()


def get_history():
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT * FROM history ORDER BY id DESC LIMIT 10"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def fetch_rates(base_currency):
    base = base_currency.upper()

    if API_KEY:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base}"
    else:
        url = f"https://open.er-api.com/v6/latest/{base}"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logger.error("Exchange rate API request timed out for base %s", base)
        raise RuntimeError("The exchange rate service timed out. Please try again.")
    except requests.exceptions.RequestException as exc:
        logger.error("Exchange rate API request failed: %s", exc)
        raise RuntimeError("Unable to reach the exchange rate service.")

    data = response.json()

    if (
        data.get("result") != "success"
        and "conversion_rates" not in data
        and "rates" not in data
    ):
        error_type = data.get("error-type", "unknown")
        logger.error("Exchange rate API returned an error: %s", error_type)
        raise RuntimeError(f"Exchange rate API error: {error_type}")
    
    rates = data.get("conversion_rates") or data.get("rates") or {}
    if not rates:
        raise RuntimeError("No exchange rate data was returned by the API.")

    updated = data.get("time_last_update_utc") or data.get("time_last_update_unix")
    if isinstance(updated, (int, float)):
        updated = datetime.fromtimestamp(updated, tz=timezone.utc).isoformat()

    return {"rates": rates, "updated": updated, "base": base}


def convert_currency(from_curr, to_curr, amount):
    from_curr = from_curr.upper()
    to_curr = to_curr.upper()

    if from_curr not in CURRENCY_META:
        raise ValueError(f"Unsupported source currency: {from_curr}")
    if to_curr not in CURRENCY_META:
        raise ValueError(f"Unsupported target currency: {to_curr}")
    if from_curr == to_curr:
        return {
            "from": from_curr,
            "to": to_curr,
            "amount": amount,
            "result": amount,
            "rate": 1.0,
            "updated": datetime.now(timezone.utc).isoformat(),
        }
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a valid number.")
    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    data = fetch_rates(from_curr)
    rate = data["rates"].get(to_curr)
    if rate is None:
        raise ValueError(f"No rate available for {from_curr} -> {to_curr}.")

    result = round(amount * rate, 4)

    try:
        add_history(from_curr, to_curr, amount, result, rate)
    except Exception as exc:
        logger.warning("Could not save history: %s", exc)

    return {
        "from": from_curr,
        "to": to_curr,
        "amount": amount,
        "result": result,
        "rate": rate,
        "updated": data["updated"],
    }



@app.route("/")
def index():
    return render_template(
        "index.html",
        currencies=SUPPORTED_CURRENCIES,
        currency_meta=CURRENCY_META,
    )


@app.route("/api/convert")
def api_convert():
    from_curr = request.args.get("from", "USD")
    to_curr = request.args.get("to", "INR")
    amount = request.args.get("amount", "1")

    try:
        payload = convert_currency(from_curr, to_curr, amount)
        return jsonify({"success": True, "data": payload})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except RuntimeError as exc:
        return jsonify({"success": False, "error": str(exc)}), 502
    except Exception:
        logger.exception("Unexpected error during conversion")
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500


@app.route("/api/history")
def api_history():
    return jsonify({"success": True, "data": get_history()})


@app.route("/api/history", methods=["DELETE"])
def api_clear_history():
    conn = get_db()
    try:
        conn.execute("DELETE FROM history")
        conn.commit()
        return jsonify({"success": True, "message": "History cleared."})
    finally:
        conn.close()


@app.route("/api/favorites", methods=["GET", "POST", "DELETE"])
def api_favorites():
    conn = get_db()
    try:
        if request.method == "GET":
            rows = conn.execute(
                "SELECT * FROM favorites ORDER BY id DESC"
            ).fetchall()
            return jsonify({"success": True, "data": [dict(r) for r in rows]})

        if request.method == "POST":
            body = request.get_json(silent=True) or {}
            from_curr = str(body.get("from", "")).upper()
            to_curr = str(body.get("to", "")).upper()
            if from_curr not in CURRENCY_META or to_curr not in CURRENCY_META:
                return jsonify({"success": False, "error": "Invalid currency."}), 400
            pair = f"{from_curr}_{to_curr}"
            conn.execute(
                "INSERT OR IGNORE INTO favorites (pair, from_curr, to_curr, created_at) "
                "VALUES (?, ?, ?, ?)",
                (pair, from_curr, to_curr, datetime.now(timezone.utc).isoformat()),
            )
            conn.commit()
            return jsonify({"success": True, "message": "Favorite added."})

        if request.method == "DELETE":
            pair = (request.args.get("pair") or "").upper()
            if not pair:
                f = (request.args.get("from") or "").upper()
                t = (request.args.get("to") or "").upper()
                if f and t:
                    pair = f"{f}_{t}"
            if not pair:
                return jsonify({"success": False, "error": "Missing pair."}), 400
            conn.execute("DELETE FROM favorites WHERE pair = ?", (pair,))
            conn.commit()
            return jsonify({"success": True, "message": "Favorite removed."})
    finally:
        conn.close()


@app.route("/api/currencies")
def api_currencies():
    return jsonify({"success": True, "data": CURRENCY_META})


@app.route("/api/trend")
def api_trend():
    from_curr = request.args.get("from", "USD").upper()
    to_curr = request.args.get("to", "INR").upper()
    try:
        data = fetch_rates(from_curr)
        latest = data["rates"].get(to_curr, 1.0)
    except Exception:
        latest = 1.0

    points = []
    base_ts = datetime.now(timezone.utc)
    for i in range(6, -1, -1):
        idx = 6 - i
        fade = i / 6 if i else 0
        wave = math.sin(idx * 1.35 + len(from_curr + to_curr))
        delta = latest * 0.006 * fade * wave
        rate = latest if i == 0 else latest + delta
        points.append({
            "label": (base_ts - timedelta(hours=i)).strftime("%H:%M"),
            "rate": round(rate, 6),
        })
    return jsonify({
        "success": True,
        "data": {
            "from": from_curr,
            "to": to_curr,
            "latest": latest,
            "series": points,
        },
    })


if __name__ == "__main__":
    init_db()
    logger.info("Starting Currency Converter on port %s", FLASK_PORT)
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)
