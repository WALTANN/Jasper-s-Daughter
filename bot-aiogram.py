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
    city = State()
  
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

                                                   # Обработчик /newcommand
@dp.message_handler(commands=['newcommand'])
async def handle_newcommand(message: types.Message):
    user_id = message.chat.id
    if not db.get_user(user_id):
        await message.answer("Вы еще не зарегистрированы. Введите /start для регистрации.")
    else:
        await NewCommand.command_name.set()
        await message.answer("Введите название новой команды:")

                                                    # Обработчик /commands
@dp.message_handler(commands=['commands'])
async def handle_commands(message: types.Message):
    user_id = message.chat.id
    user = db.get_user(user_id)
    if user:
        commands = db.get_commands(user_id)
        if commands:
            response = "Ваши команды:\n" + "\n".join([f"{cmd['name']} - {cmd['url']}" for cmd in commands])
        else:
            response = "У вас нет сохраненных команд."
        await message.answer(response)
    else:
        await message.answer("Сначала зарегистрируйтесь с помощью /start.")
      
                                                    # Обработчик /deletecommand
@dp.message_handler(commands=['deletecommand'])
async def handle_delete_command(message: types.Message):
    user_id = message.chat.id
    if not db.get_user(user_id):
        await message.answer("Вы еще не зарегистрированы. Введите /start для регистрации.")
    else:
        await DeleteCommand.command_name.set()
        await message.answer("Введите название команды, которую хотите удалить:")
        
                                                    # Обработчик /deleteprofile
@dp.message_handler(commands=['deleteprofile'])
async def handle_delete_user(message: types.Message):
    user_id = message.chat.id
    if not db.get_user(user_id):
        await message.answer("Вы еще не зарегистрированы.")
    else:
        try:
            db.delete_user(user_id)
            await message.answer("Ваш аккаунт успешно удален.")
        except ValueError as e:
            await message.answer(str(e))

                                                    # Обработчик /checkusers
@dp.message_handler(commands=['checkusers'])
async def handle_checkusers(message: types.Message):
    user_id = message.chat.id
    if str(user_id) == str(config.ADMIN):
        users = db.get_all_users()
        if not users:
            await message.answer("В базе данных нет зарегистрированных пользователей.")
        else:
            users_list = "\n".join([f"{user_id}: {name}" for user_id, name in users.items()])
            await message.answer(f"Зарегистрированные пользователи:\n{users_list}")
    else:
        await message.answer(f"Такой команды нет, введите /help")



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
    await state.update_data(password=message.text)
    await Registration.next()
    await message.answer("Теперь введите ваш город:")
    
@dp.message_handler(state=Registration.city)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text

        user_id = message.chat.id
        name = data['name']
        login = data['login']
        password = data['password']
        city = data['city']

        try:
            db.add_user(user_id, name, login, password, city)
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

                                                    # Обработчики добавления newcommand
@dp.message_handler(state=NewCommand.command_name)
async def process_command_name(message: types.Message, state: FSMContext):
    await state.update_data(command_name=message.text)
    await NewCommand.next()
    await message.answer("Введите URL для новой команды:")

@dp.message_handler(state=NewCommand.command_url)
async def process_command_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = message.chat.id
        command_name = data['command_name']
        command_url = message.text
        try:
            db.add_command(user_id, command_name, command_url)
            await message.answer(f"Команда '{command_name}' успешно добавлена с URL: {command_url}")
        except ValueError as e:
            await message.answer(str(e))
    
    await state.finish()

                                                    # Обработчик deletecommand
@dp.message_handler(state=DeleteCommand.command_name)
async def process_delete_command(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    command_name = message.text
    try:
        db.delete_command(user_id, command_name)
        await message.answer(f"Команда '{command_name}' успешно удалена.")
    except ValueError as e:
        await message.answer(str(e))
    
    await state.finish()

@dp.message_handler()
async def handle_text(message: types.Message):
    await message.answer(f"Такой команды нет, введите /help")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
