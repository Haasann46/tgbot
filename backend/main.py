from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from backend.utils.telegram_auth import check_telegram_auth
from bot.config import BOT_TOKEN
print("🔥 REAL BACKEND LOADED 🔥")
print("🔥 BACKEND MAIN LOADED 🔥")

app = FastAPI()


# =========================
# MINI APP HTML
# =========================
@app.get("/app")
async def mini_app():
    with open("backend/static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


# =========================
# AUTH API
# =========================
class AuthRequest(BaseModel):
    initData: str


@app.post("/api/auth")
async def auth(data: dict):
    print("🔥 AUTH CALLED 🔥")
    print(data)
    return {"ok": True}