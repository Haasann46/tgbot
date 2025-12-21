from aiogram import Router, F
from aiogram.types import Message
from bot.database.db import cursor, conn
from datetime import datetime
from bot.handlers.states import IncomeState
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text == "➕ Добавить доход")
async def add_income(message: Message):
    await message.answer("💸 Введите сумму доходов:")

@router.message(F.text.regexp(r"^\d+$"))
async def save_income(message: Message, state: FSMContext):
    await state.set_state(IncomeState.amount)
    amount = int(message.text)
    user_id = message.from_user.id

    cursor.execute(
        "INSERT INTO transactions (user_id, amount, type, category, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, "income", "Другое", datetime.now().isoformat())
    )
    conn.commit()

    await message.answer("✅ доход сохранён!")
