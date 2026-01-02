from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.database.db import get_connection
from bot.handlers.states import NotesState
from bot.keyboards.reply import (
    notes_keyboard,
    main_keyboard,
    confirm_delete_notes_keyboard
)

router = Router()

# ─────────────────────────────────────────────
# ВХОД В ЗАМЕТКИ
# ─────────────────────────────────────────────

@router.message(F.text == "🧾 Заметки")
async def notes_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🧾 Меню заметок:",
        reply_markup=notes_keyboard
    )

# ─────────────────────────────────────────────
# ДОБАВЛЕНИЕ ЗАМЕТКИ
# ─────────────────────────────────────────────

@router.message(F.text == "➕ Добавить заметку")
async def add_note(message: Message, state: FSMContext):
    await state.set_state(NotesState.text)
    await message.answer("✏️ Введите текст заметки:")

@router.message(NotesState.text)
async def save_note(message: Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (user_id, text) VALUES (?, ?)",
        (user_id, text)
    )

    conn.commit()
    conn.close()

    await state.clear()
    await message.answer(
        "✅ Заметка сохранена",
        reply_markup=notes_keyboard
    )

# ─────────────────────────────────────────────
# ПРОСМОТР ЗАМЕТОК
# ─────────────────────────────────────────────

@router.message(F.text == "📋 Мои заметки")
async def show_notes(message: Message):
    user_id = message.from_user.id

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT text FROM notes WHERE user_id = ?",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        await message.answer("📭 У вас пока нет заметок")
        return

    text = "🧾 Ваши заметки:\n\n"
    for i, row in enumerate(rows, start=1):
        text += f"{i}. {row[0]}\n"

    await message.answer(text)

# ─────────────────────────────────────────────
# УДАЛЕНИЕ ЗАМЕТОК
# ─────────────────────────────────────────────

@router.message(F.text == "🗑 Удалить заметки")
async def delete_notes_confirm(message: Message):
    await message.answer(
        "⚠️ Вы уверены, что хотите удалить ВСЕ заметки?",
        reply_markup=confirm_delete_notes_keyboard
    )

@router.message(F.text == "✅ Да, удалить всё")
async def delete_notes(message: Message):
    user_id = message.from_user.id

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE user_id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    await message.answer(
        "🗑 Все заметки удалены",
        reply_markup=notes_keyboard
    )

@router.message(F.text == "❌ Отмена")
async def cancel_delete_notes(message: Message):
    await message.answer(
        "❌ Удаление отменено",
        reply_markup=notes_keyboard
    )

# ─────────────────────────────────────────────
# ВОЗВРАТ В ГЛАВНОЕ МЕНЮ
# ─────────────────────────────────────────────

@router.message(F.text == "⬅ Назад")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🏠 Главное меню",
        reply_markup=main_keyboard
    )
