import os, time, requests
from telethon import events
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# --- ENV ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

# Approver (Railway)
RAILWAY_HOST = os.getenv("RAILWAY_HOST", "https://a1click-production.up.railway.app").rstrip("/")
AUTH_TOKEN   = os.getenv("AUTH_TOKEN", "")

# Chat-Filter (entweder CHAT_IDS ODER CHAT_ID/CHAT_TITLE)
CHAT_IDS   = [s.strip() for s in os.getenv("CHAT_IDS", "").split(",") if s.strip()]
CHAT_ID    = os.getenv("CHAT_ID", "")
CHAT_TITLE = os.getenv("CHAT_TITLE", "")

# Optional: kleine Entprellung, doppelte Events in kurzer Zeit unterdrücken
DEBOUNCE_SECONDS = int(os.getenv("DEBOUNCE_SECONDS", "3"))

# --- Telegram Client ---
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

def match_chat(e):
    if CHAT_IDS:
        cid = str(e.chat_id)
        title = getattr(e.chat, "title", "") or getattr(e.chat, "first_name", "")
        for x in CHAT_IDS:
            if x.startswith("@"):
                if title == x.lstrip("@"):
                    return True
            elif x == cid:
                return True
        return False
    if CHAT_ID and str(e.chat_id) != str(CHAT_ID):
        return False
    if CHAT_TITLE:
        c = e.chat
        t = getattr(c, "title", "")
        f = getattr(c, "first_name", "")
        return (t == CHAT_TITLE) or (f == CHAT_TITLE)
    return True

_last_ts = 0.0

@client.on(events.NewMessage())
async def handler(e):
    global _last_ts
    if not match_chat(e):
        return

    now = time.monotonic()
    if now - _last_ts < DEBOUNCE_SECONDS:
        return
    _last_ts = now

    try:
        r = requests.get(
            f"{RAILWAY_HOST}/approve",
            params={"auth": AUTH_TOKEN},
            timeout=30
        )
        text = r.text
        try:
            js = r.json()
            text = f"Approve → {js}"
        except Exception:
            pass
        try:
            await e.respond(text)
        except Exception:
            pass
        print("Approve response:", r.text)
    except Exception as ex:
        print("Approve error:", ex)

# === Neues Feature: alle Dialoge einmal anzeigen ===
async def list_dialogs():
    print("📋 Alle Dialoge/Chats:")
    async for dialog in client.iter_dialogs():
        print(f"{dialog.id} | {dialog.title or dialog.name or dialog.entity.username}")

client.start()
client.loop.run_until_complete(list_dialogs())
print("Listening…")
client.run_until_disconnected()
