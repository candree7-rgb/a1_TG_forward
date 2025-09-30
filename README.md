# tg-forwarder-a1click

Minimaler **Telegram-Forwarder** (Telethon):  
Neue Nachricht in ausgewählten Chats → **ruft Approver** auf Railway:
`GET /approve?auth=<TOKEN>`

## Setup

1) Repo clonen und `.env` aus `.env.example` erstellen & füllen:
- `API_ID`, `API_HASH` → https://my.telegram.org
- `STRING_SESSION` → Telethon-Session (dein bisheriger String funktioniert)
- Filter setzen: `CHAT_IDS` (z.B. `@AlgosoneBot`) **oder** `CHAT_ID` **oder** `CHAT_TITLE`
- `RAILWAY_HOST` → deine Approver-URL
- `AUTH_TOKEN` → Token, den Approver prüft

2) Lokal testen
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python forwarder.py
