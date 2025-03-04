from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from .forms import RegistrationDialog
from ...application.services.user_service import RegistrationService

class RegistrationHandler:
    def __init__(self, registration_service: RegistrationService):
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
        dp.register_message_handler(self.start_registration, Command("register"), state="*") #Состояние "*" позволяет запускать команду из любого места.
        dp.register_message_handler(self.process_name, state=RegistrationDialog.waiting_for_name)
        dp.register_message_handler(self.process_phone, state=RegistrationDialog.waiting_for_phone)