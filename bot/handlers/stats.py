from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime, timedelta

from bot.database.db import get_connection

router = Router()


@router.message(F.text == "📊 Статистика")
async def stats_7_days(message: Message):
    user_id = message.from_user.id

    date_from = (datetime.now() - timedelta(days=7)).isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    # ➕ доходы
    cursor.execute(
        """
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ?
        AND type = 'income'
        AND created_at >= ?
        """,
        (user_id, date_from)
    )
    income = cursor.fetchone()[0] or 0

    # ➖ расходы
    cursor.execute(
        """
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ?
        AND type = 'expense'
        AND created_at >= ?
        """,
        (user_id, date_from)
    )
    expense = cursor.fetchone()[0] or 0

    conn.close()

    balance = income - expense

    await message.answer(
        f"📊 Статистика за 7 дней\n\n"
        f"➕ Доходы: {income}\n"
        f"➖ Расходы: {expense}\n"
        f"💰 Баланс: {balance:+}"
    )
