from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➖ Добавить расход"),
            KeyboardButton(text="➕ Добавить доход")
        ],
        [
            KeyboardButton(text="📊 Статистика")
        ]
    ],
    resize_keyboard=True
)
