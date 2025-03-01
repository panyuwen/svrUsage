from flask import Flask, jsonify, send_file
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

LOG_FILE = "server_usage.csv"

@app.route("/data")
def get_data():
    try:
        df = pd.read_csv(LOG_FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Get data for the last 24 hours
        cutoff = datetime.now() - timedelta(hours=24)
        df = df[df["timestamp"] >= cutoff]

        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/")
def index():
    return send_file("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)