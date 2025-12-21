from aiogram import Router, F
from aiogram.types import Message
from bot.database.db import cursor, conn
from datetime import datetime
from bot.handlers.states import ExpenseState
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(F.text == "➖ Добавить расход")
async def add_expense(message: Message, state: FSMContext):
    await state.clear()  # ✅ сброс любого старого состояния
    await state.set_state(ExpenseState.amount)  # ✅ ВКЛЮЧАЕМ FSM
    await message.answer("💸 Введите сумму расхода:")


@router.message(ExpenseState.amount)
async def save_expense(message: Message, state: FSMContext):
    amount = int(message.text)
    user_id = message.from_user.id

    cursor.execute(
        "INSERT INTO transactions (user_id, amount, type, category, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, "expense", "Другое", datetime.now().isoformat())
    )
    conn.commit()

    await message.answer("✅ Расход сохранён!")
    await state.clear()  # ✅ очищаем ПОСЛЕ сохранения
