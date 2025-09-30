import os, requests
from telethon import events
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

RAILWAY_HOST = os.getenv("RAILWAY_HOST", "https://a1click-production.up.railway.app").rstrip("/")
AUTH_TOKEN   = os.getenv("AUTH_TOKEN", "")

CHAT_ID    = os.getenv("CHAT_ID", "")
CHAT_TITLE = os.getenv("CHAT_TITLE", "")

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

# === Chat-ID Finder ===
async def list_dialogs():
    print("📋 Alle Dialoge/Chats:")
    async for dialog in client.iter_dialogs():
        print(f"{dialog.id} | {dialog.title or dialog.name or dialog.entity.username}")

def match_chat(e):
    if CHAT_ID and str(e.chat_id) != str(CHAT_ID):
        return False
    if CHAT_TITLE:
        c = e.chat
        t = getattr(c, "title", "")
        f = getattr(c, "first_name", "")
        return (t == CHAT_TITLE) or (f == CHAT_TITLE)
    return True

@client.on(events.NewMessage())
async def handler(e):
    if not match_chat(e):
        return
    try:
        requests.post(
            f"{RAILWAY_HOST}/hook/telegram",
            headers={"x-auth": AUTH_TOKEN} if AUTH_TOKEN else {},
            json={
                "message": e.raw_text or "",
                "chat_id": e.chat_id,
                "msg_id": e.id,
                "date": str(e.date)
            },
            timeout=8
        )
    except Exception as ex:
        print("Webhook error:", ex)

client.start()
client.loop.run_until_complete(list_dialogs())  # 👈 IDs ausgeben
print("Listening…")
client.run_until_disconnected()
