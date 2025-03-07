from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import bold

from modules.user.application.services.user_service import UserService
from .forms import RegistrationDialog


class StartHandler:
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def start(self, message: types.Message):
        """
        This handler receives messages with `/start` command
        """
        chat_id = message.chat.id
        await message.answer(f"Bot ID: {self.bot.id}")
        await message.answer(f"Chat ID: {chat_id}")
        await message.answer(f"User ID: {bold(message.from_user.id)}")
        await message.answer(f"User name: {bold(message.from_user.full_name)}")
        await message.answer("")
        await message.answer(f"Привет, {message.from_user.first_name}! Я помогу тебе зарегистрироваться.")
        await RegistrationDialog.ask_name(message)

    def register_hadlers(self, dp: Dispatcher):
        dp.message.register(self.start, CommandStart())


class RegistrationHandler:
    def __init__(self, registration_service: UserService):
        self.registration_service = registration_service

    async def start_registration(self, message: types.Message, state: FSMContext):
        """Обработчик команды /register, начало регистрации."""
        user_id = message.from_user.id
        self.registration_service.start_registration(user_id) #Сохранение user_id
        await RegistrationDialog.ask_name(message)

    async def process_name(self, message: types.Message, state: FSMContext):
        """Обработчик ввода имени и фамилии."""
        name = message.text
        async with state.proxy() as data:
            data['name'] = name
        await RegistrationDialog.ask_phone(message)

    async def process_phone(self, message: types.Message, state: FSMContext):
        """Обработчик ввода номера телефона."""
        phone = message.text
        async with state.proxy() as data:
            data['phone'] = phone
        self.registration_service.complete_registration(data, message.from_user.id) #Завершение регистрации
        await RegistrationDialog.complete(message)

    def register_handlers(self, dp: Dispatcher):
        """Регистрация обработчиков."""
        dp.message.register(self.start_registration, Command("register"), state="*") #Состояние "*" позволяет запускать команду из любого места.
        dp.message.register(self.process_name, state=RegistrationDialog.waiting_for_name)
        dp.message.register(self.process_phone, state=RegistrationDialog.waiting_for_phone)