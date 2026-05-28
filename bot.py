import os
import time
import threading
import requests
from flask import Flask

# ---------------- FLASK ----------------
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'


def run_web():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# ---------------- TOKENS ----------------
TELEGRAM_TOKEN = os.environ.get('8977689607:AAGv2VwqlsOSqmBXK3JgH1P3z8tepoHLULQ')
GROQ_API_KEY = os.environ.get('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')

URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}'

# ---------------- AI ----------------
def ask_ai(text):
    try:
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama-3.1-8b-instant',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'Ты умный и дружелюбный AI ассистент.'
                    },
                    {
                        'role': 'user',
                        'content': text
                    }
                ]
            },
            timeout=20
        )

        data = response.json()

        return data['choices'][0]['message']['content']

    except Exception as e:
        print('AI ERROR:', e)
        return 'Ошибка AI 😢'

# ---------------- BOT ----------------
offset = None

def run_bot():
    global offset
    print("🤖 BOT STARTED")

    while True:
        try:
            print("CHECKING UPDATES...")

            res = requests.get(
                URL + f"/getUpdates?timeout=10&offset={offset}",
                timeout=15
            ).json()

            print("RESPONSE:", res)

            for update in res.get("result", []):
                offset = update["update_id"] + 1

                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"].get("text", "")

                    print("MESSAGE:", text)

                    requests.get(
                        URL + "/sendMessage",
                        params={
                            "chat_id": chat_id,
                            "text": text
                        }
                    )

            time.sleep(1)

        except Exception as e:
            print("ERROR:", e)
            time.sleep(2)

# ---------------- START ----------------
threading.Thread(target=run_web).start()
run_bot()
