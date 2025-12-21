from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➖ Добавить расход"),
            KeyboardButton(text="➕ Добавить доход")
        ],
        [
            KeyboardButton(text="📊 Статистика")
        ],
        [ KeyboardButton(text="Обнулить статистику")
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