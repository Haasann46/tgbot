from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import datetime

from bot.database.db import get_connection
from bot.handlers.states import ExpenseState
from bot.keyboards.reply import cancel_keyboard, main_keyboard

router = Router()


@router.message(F.text == "➖ Добавить расход")
async def add_expense(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ExpenseState.amount)

    await message.answer(
        "💸 Введите сумму расхода:",
        reply_markup=cancel_keyboard
    )


@router.message(ExpenseState.amount)
async def save_expense(message: Message, state: FSMContext):
    # обработка отмены
    if message.text == "⬅ Назад":
        await state.clear()
        await message.answer(
            "❌ Добавление расхода отменено",
            reply_markup=main_keyboard
        )
        return

    # проверка ввода
    if not message.text.isdigit():
        await message.answer(
            "❗ Введите сумму цифрами или нажмите «⬅ Назад»"
        )
        return

    amount = int(message.text)
    user_id = message.from_user.id

    # работа с БД
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (user_id, amount, type, category, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, amount, "expense", "Другое", datetime.now().isoformat())
    )

    conn.commit()
    conn.close()

    await state.clear()
    await message.answer(
        "✅ Расход сохранён!",
        reply_markup=main_keyboard
    )
