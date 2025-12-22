from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.keyboards.reply import main_keyboard
from bot.database.db import get_connection

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    name = message.from_user.first_name

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)",
        (user_id, name)
    )

    conn.commit()
    conn.close()

    await message.answer(
        f"👋 Привет, {name}!\nЯ помогу вести учёт твоих финансов 💰",
        reply_markup=main_keyboard
    )
