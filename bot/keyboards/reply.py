from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# ⚠️ ВАЖНО: вставь СВОЙ HTTPS от ngrok
MINI_APP_URL = 'https://jadon-nonamphibian-elmer.ngrok-free.dev/app'


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➖ Добавить расход"),
            KeyboardButton(text="➕ Добавить доход")
        ],
        [
            KeyboardButton(text="📊 Статистика"),
            KeyboardButton(text="🧾 Заметки")
        ],
        [
            KeyboardButton(
                text="🚀 Mini App",
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
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
        [KeyboardButton(text="➕ Добавить заметку")],
        [KeyboardButton(text="📋 Мои заметки")],
        [KeyboardButton(text="🗑 Удалить заметки")],
        [KeyboardButton(text="⬅ Назад")]
    ],
    resize_keyboard=True
)


confirm_delete_notes_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Да, удалить всё")],
        [KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)
