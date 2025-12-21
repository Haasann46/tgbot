from aiogram import Router, F
from aiogram.types import Message
from bot.database.db import cursor, conn

router = Router()

@router.message(F.text == "Обнулить статистику")
async def reset_stats(message: Message):
    user_id = message.from_user.id

    cursor.execute(
        "UPDATE transactions SET amount = 0 WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()

    await message.answer("✅ Статистика успешно обнулена")
