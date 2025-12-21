from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import datetime

from bot.database.db import cursor, conn
from bot.handlers.states import IncomeState
from bot.keyboards.reply import cancel_keyboard, main_keyboard

router = Router()  # ❗ ОБЯЗАТЕЛЬНО ДО ДЕКОРАТОРОВ


@router.message(F.text == "➕ Добавить доход")
async def add_income(message: Message, state: FSMContext):
    # сбрасываем любое старое состояние
    await state.clear()
    # включаем FSM
    await state.set_state(IncomeState.amount)

    await message.answer(
        "💰 Введите сумму дохода:",
        reply_markup=cancel_keyboard
    )


@router.message(IncomeState.amount)
async def save_income(message: Message, state: FSMContext):
    # ⬅ КНОПКА НАЗАД
    if message.text == "⬅ Назад":
        await state.clear()
        await message.answer(
            "❌ Добавление дохода отменено",
            reply_markup=main_keyboard
        )
        return

    # ❌ если ввели не число или нажали другую кнопку
    if not message.text.isdigit():
        await message.answer(
            "❗ Введите сумму цифрами или нажмите «⬅ Назад»"
        )
        return

    # ✅ корректный ввод
    amount = int(message.text)
    user_id = message.from_user.id

    cursor.execute(
        "INSERT INTO transactions (user_id, amount, type, category, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, "income", "Другое", datetime.now().isoformat())
    )
    conn.commit()

    await state.clear()
    await message.answer(
        "✅ Доход сохранён!",
        reply_markup=main_keyboard
    )
