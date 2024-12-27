import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardMarkup
from module_13.config import TOKEN

# Инициализация бота и создание диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создание состояния пользователя
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight =State()


# Создание меню клавиатуры
keyboard_start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')],
        [KeyboardButton(text='Купить')]
    ],
    resize_keyboard=True
)

# Создание инлайн клавиатур
inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
        ]
    ]
)

inline_keyboard_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Вернуться в меню', callback_data='back to menu')]
    ]
)

inline_keyboard_products = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Продукт 1', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт 2', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт 3', callback_data='product_buying'),
         InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')],
    ]
)

# Обработчик команды /start
@dp.message(CommandStart())
async def start_message(message: Message):
    await message.reply('Привет! Я бот помогающий твоему здоровью.',  reply_markup=keyboard_start)


# Обработчик сообщения
@dp.message(F.text == 'Рассчитать')
async def main_menu(message: Message):
    await message.reply(text='Выберите опцию', reply_markup=inline_keyboard)


@dp.message(F.text == 'Купить')
async def get_buying_list(message: Message):
    await message.answer_photo(photo='https://cdn.orteka.ru//upload/resize_cache/iblock/901/1200_1200_1d8f616e6dafd84ca6b85089cc850afe3/l18eywjremq294be2by9zesfvlavrzx8.png', caption='Гидролизат коллагена усиленная формула с эластином, 1 кг')
    await message.answer_photo(photo='https://cdn.orteka.ru//upload/resize_cache/iblock/b3b/624_624_1d8f616e6dafd84ca6b85089cc850afe3/fydcv6cis3i6hybmkjnqf98e8t0zwisu.jpg', caption='Витамины для здоровья сосудов и вен VIPROACTIVE Ven Pro , капс. 60 шт.')
    await message.answer_photo(photo='https://cdn.orteka.ru//upload/resize_cache/iblock/bf2/1200_1200_1d8f616e6dafd84ca6b85089cc850afe3/1jbg0e6qxcer439j6t35j1dm73io30mv.jpg', caption='Натуральный комплекс " Здоровые вены" содержит диосмин и комплекс цитрусовых биофлаваноидов, 60 капсул')
    await message.answer_photo(photo='https://cdn.orteka.ru//upload/resize_cache/iblock/ef0/624_624_1d8f616e6dafd84ca6b85089cc850afe3/fnscmtxue3udfvlp6w7o6i1z6vhbjm4e.jpg', caption='БАД Навимесо Коллаген Джойнтс (Navimeso Collagen Joints)')
    await message.answer(text='Выберите продукт для покупки:', reply_markup=inline_keyboard_products)


# Обработчик инлайн кнопки
@dp.callback_query(F.data == 'formulas')
async def get_formulas(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer(text='Формула: 10 х Вес (кг) + 6.25 * Рост (см) - 5 * Возраст (г)', reply_markup=inline_keyboard_back)


@dp.callback_query(F.data == 'product_buying')
async def send_confirm_message(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text='Вы успешно приобрели продукт!')


@dp.callback_query(F.data == 'back to menu')
async def back_to_menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer(text='Выберите опцию', reply_markup=inline_keyboard)


@dp.callback_query(F.data.lower() == 'calories')
async def set_age(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.age)
    await callback.answer('')
    await callback.message.answer(text="Введите свой возраст:")


# Обработчик изменения состояния age
@dp.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age = message.text)
    await state.set_state(UserState.growth)
    await message.answer('Введите свой рост:')


# Обработчик изменения состояния growth
@dp.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth = message.text)
    await state.set_state(UserState.weight)
    await message.answer('Введите свой вес:')


# Обработчик изменения состояния weight
@dp.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    age, weight, growth = list(data.values())
    result = 10 * int(weight) + 6.25 * int(growth) - 5 * int(age)
    await message.reply(f'Ваша норма калорий: {result}', reply_markup=inline_keyboard_back)
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')