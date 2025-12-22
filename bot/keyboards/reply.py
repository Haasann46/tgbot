from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➖ Добавить расход"),
            KeyboardButton(text="➕ Добавить доход")
        ],
        [
            KeyboardButton(text="📊 Статистика"),
            KeyboardButton(text="📝 Заметки")
        ],
        [
            KeyboardButton(text="Обнулить статистику")
        ]
    ],
    resize_keyboard=True
)


cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬅ Назад")]
    ],
    resize_keyboard=True
)


notes_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Добавить заметку"),
            KeyboardButton(text="📋 Посмотреть заметки")
        ],
        [
            KeyboardButton(text="❌ Удалить заметку по номеру"),
            KeyboardButton(text="🗑 Удалить все заметки")
        ],
        [
            KeyboardButton(text="⬅ Назад")
        ]
    ],
    resize_keyboard=True
)


confirm_delete_notes_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Да, удалить"),
            KeyboardButton(text="❌ Отмена")
        ]
    ],
    resize_keyboard=True
)
