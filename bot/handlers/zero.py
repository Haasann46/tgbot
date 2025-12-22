from aiogram import Router, F
from aiogram.types import Message

from bot.database.db import get_connection

router = Router()


@router.message(F.text == "Обнулить статистику")
async def reset_stats(message: Message):
    user_id = message.from_user.id

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE transactions SET amount = 0 WHERE user_id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    await message.answer("✅ Статистика успешно обнулена")
