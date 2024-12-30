from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from gevent.libev.corecext import callback

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Стоимость'),
            KeyboardButton(text='О нас')
        ]
    ],
    resize_keyboard=True
)

catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Средняя игра', callback_data='medium')],
        [InlineKeyboardButton(text='Большая игра', callback_data='big')],
        [InlineKeyboardButton(text='Очень большая игра', callback_data='mega')],
        [InlineKeyboardButton(text='Другие предложения', callback_data='other')],
    ]
)

buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Купить', url='https://ya.ru')],
        [InlineKeyboardButton(text='Назад', callback_data='back_to_catalog')]
    ]
)

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Пользователи', callback_data='users')],
        [InlineKeyboardButton(text='Статистика', callback_data='stat')],
        [
            InlineKeyboardButton(text='Блокировка', callback_data='block'),
            InlineKeyboardButton(text='Разблокировка', callback_data='unblock')
        ]
    ]
)