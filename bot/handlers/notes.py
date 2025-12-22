from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import datetime

from bot.keyboards.reply import (
    notes_keyboard,
    main_keyboard,
    cancel_keyboard,
    confirm_delete_notes_keyboard
)
from bot.database.db import get_connection
from bot.handlers.states import NotesState

router = Router()


# Вход в меню заметок
@router.message(F.text == "📝 Заметки")
async def open_notes_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "📝 Меню заметок",
        reply_markup=notes_keyboard
    )


# Назад в главное меню
@router.message(F.text == "⬅ Назад")
async def back_to_main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Главное меню",
        reply_markup=main_keyboard
    )


# ➕ Добавить заметку
@router.message(F.text == "➕ Добавить заметку")
async def add_note_start(message: Message, state: FSMContext):
    await state.set_state(NotesState.text)
    await message.answer(
        "✍️ Введите текст заметки:",
        reply_markup=cancel_keyboard
    )


@router.message(NotesState.text)
async def add_note_save(message: Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (user_id, text, created_at) VALUES (?, ?, ?)",
        (user_id, text, datetime.now().isoformat())
    )
    conn.commit()

    cursor.execute(
        "SELECT COUNT(*) FROM notes WHERE user_id = ?",
        (user_id,)
    )
    note_number = cursor.fetchone()[0]

    conn.close()

    await message.answer(
        f"✅ Заметка №{note_number} сохранена",
        reply_markup=notes_keyboard
    )
    await state.clear()


# 📋 Посмотреть заметки
@router.message(F.text == "📋 Посмотреть заметки")
async def show_notes(message: Message):
    user_id = message.from_user.id

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT text FROM notes WHERE user_id = ? ORDER BY id",
        (user_id,)
    )
    notes = cursor.fetchall()

    conn.close()

    if not notes:
        await message.answer(
            "У вас пока нет заметок",
            reply_markup=notes_keyboard
        )
        return

    result = ""
    for i, (note_text,) in enumerate(notes, start=1):
        result += f"📝 Заметка {i}\n{note_text}\n\n"

    await message.answer(
        result,
        reply_markup=notes_keyboard
    )


# ❌ Удалить заметку по номеру
@router.message(F.text == "❌ Удалить заметку по номеру")
async def delete_note_start(message: Message, state: FSMContext):
    await state.set_state(NotesState.delete_number)
    await message.answer(
        "🔢 Введите номер заметки, которую хотите удалить:",
        reply_markup=cancel_keyboard
    )


@router.message(NotesState.delete_number)
async def delete_note_finish(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()

    if not text.isdigit():
        await message.answer("❌ Введите корректный номер (число)")
        return

    note_number = int(text)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM notes WHERE user_id = ? ORDER BY id",
        (user_id,)
    )
    notes = cursor.fetchall()

    if not notes:
        conn.close()
        await message.answer(
            "У вас нет заметок для удаления",
            reply_markup=notes_keyboard
        )
        await state.clear()
        return

    if note_number < 1 or note_number > len(notes):
        conn.close()
        await message.answer(
            f"❌ Неверный номер. Введите число от 1 до {len(notes)}"
        )
        return

    note_id = notes[note_number - 1][0]

    cursor.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )
    conn.commit()
    conn.close()

    await message.answer(
        f"✅ Заметка №{note_number} удалена",
        reply_markup=notes_keyboard
    )
    await state.clear()


# 🗑 Удалить все заметки (подтверждение)
@router.message(F.text == "🗑 Удалить все заметки")
async def delete_all_notes_confirm(message: Message):
    await message.answer(
        "⚠️ Вы уверены, что хотите удалить ВСЕ заметки?",
        reply_markup=confirm_delete_notes_keyboard
    )


@router.message(F.text == "✅ Да, удалить")
async def delete_all_notes(message: Message):
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
