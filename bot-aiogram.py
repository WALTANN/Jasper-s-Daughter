import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from DB.database import Database
import settings.config as config


                                                    # Файл БД
filename = "users.json"

                                                    # экземпляр БД
db = Database(filename)

                                                    # Инициализация бота
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

                                                    # FSM
class Registration(StatesGroup):
    name = State()
    login = State()
    password = State()

class UpdatePassword(StatesGroup):
    new_password = State()

class UpdateUsername(StatesGroup):
    new_username = State()

class NewCommand(StatesGroup):
    command_name = State()
    command_url = State()

class DeleteCommand(StatesGroup):
    command_name = State()

                                                    # Обработчик /start
@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    user_id = message.chat.id
    if db.get_user(user_id):
        await message.answer("Вы уже зарегистрированы.")
    else:
        await Registration.name.set()
        await message.answer("Привет! Для регистрации введите ваше имя:")

                                                    # Обработчик /help
@dp.message_handler(commands=['help'])
async def handle_start(message: types.Message):
    user_id = message.chat.id
    if db.get_user(user_id):
        if str(user_id) == str(config.ADMIN):
            await message.answer(config.ADMIN_HELP_MESSAGE)
        else:
            await message.answer(config.HELP_MASSEGE)
    else:
        await Registration.name.set()
        await message.answer("Привет! Для регистрации введите ваше имя:")
                                                    # Обработчик /uppass
@dp.message_handler(commands=['uppass'])
async def handle_uppass(message: types.Message):
    user_id = message.chat.id
    if not db.get_user(user_id):
        await message.answer("Вы еще не зарегистрированы. Введите /start для регистрации.")
    else:
        await UpdatePassword.new_password.set()
        await message.answer("Введите ваш новый пароль:")

                                                    # Обработчик /upusername
@dp.message_handler(commands=['upusername'])
async def handle_upusername(message: types.Message):
    user_id = message.chat.id
    if not db.get_user(user_id):
        await message.answer("Вы еще не зарегистрированы. Введите /start для регистрации.")
    else:
        await UpdateUsername.new_username.set()
        await message.answer("Введите ваше новое имя пользователя:")




                                                    # Обработчики FSM
                                                    # Обработчки регистрации
@dp.message_handler(state=Registration.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await Registration.next()
    await message.answer("Теперь введите ваш логин:")

@dp.message_handler(state=Registration.login)
async def process_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await Registration.next()
    await message.answer("Теперь введите ваш пароль:")

@dp.message_handler(state=Registration.password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text

        user_id = message.chat.id
        name = data['name']
        login = data['login']
        password = data['password']

        try:
            db.add_user(user_id, name, login, password)
            await message.answer("Регистрация успешно завершена!")
        except ValueError as e:
            await message.answer(str(e))
    
    await state.finish()

                                                    # Обработчики обновления пароля
@dp.message_handler(state=UpdatePassword.new_password)
async def process_new_password(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    new_password = message.text
    try:
        db.update_password(user_id, new_password)
        await message.answer("Ваш пароль успешно обновлен!")
    except ValueError as e:
        await message.answer(str(e))
    
    await state.finish()

                                                    # Обработчики обновления username
@dp.message_handler(state=UpdateUsername.new_username)
async def process_new_username(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    new_username = message.text
    try:
        db.update_username(user_id, new_username)
        await message.answer("Ваше имя пользователя успешно обновлено!")
    except ValueError as e:
        await message.answer(str(e))
    
    await state.finish()

@dp.message_handler()
async def handle_text(message: types.Message):
    await message.answer(f"Такой команды нет, введите /help")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
