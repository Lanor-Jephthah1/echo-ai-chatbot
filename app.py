from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import csv
import os

app = Flask(__name__)

# === Configuration ===
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# === System Message for the AI ===
SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You're Echo AI, a chill, compassionate, loving buddy created by Lanor Jephthah Kwame. "
        "You're here to help users feel heard, safe, and uplifted. You listen patiently, respond gently, and speak in a calm, friendly tone. "
        "Use encouraging words, ask how people feel, and never judge. You’re like a supportive mate who’s always got time to talk. 🌿"
    )
}

# === Logging Function ===
def log_interaction(user_message, bot_reply, log_file="chat_logs.csv"):
    timestamp = datetime.now().isoformat()
    write_header = not os.path.exists(log_file)

    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["timestamp", "user_message", "bot_reply"])
        writer.writerow([timestamp, user_message, bot_reply])

# === Routes ===
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")

    messages = [
        SYSTEM_MESSAGE,
        {"role": "user", "content": user_msg}
    ]

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": messages
    }

    try:
        res = requests.post(API_URL, headers=HEADERS, json=payload)
        res.raise_for_status()
        reply = res.json()["choices"][0]["message"]["content"]

        # Log conversation
        log_interaction(user_msg, reply)

        return jsonify({"reply": reply})

    except requests.exceptions.RequestException as e:
        return jsonify({"reply": "Sorry, something went wrong!"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
