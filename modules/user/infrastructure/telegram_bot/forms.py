from aiogram.fsm.state import State, StatesGroup
from aiogram import types
from aiogram.fsm.context import FSMContext

class RegistrationDialog(StatesGroup):
    """Class for managing the state of the user registration dialog."""

    waiting_for_name = State()
    """Waiting for first and last name to be entered."""

    waiting_for_phone = State()
    """Waiting for phone number."""

    registration_complete = State()
    """Registration is complete, waiting for commands."""

    async def ask_name(self, message: types.Message, state: FSMContext):
        """Запрос имени и фамилии."""
        await state.set_state(RegistrationDialog.waiting_for_name)
        await message.reply("Введите ваше имя и фамилию:")

    async def ask_phone(self, message: types.Message, state: FSMContext):
        """Запрос номера телефона."""
        await state.set_state(RegistrationDialog.waiting_for_phone)
        await message.reply("Введите ваш номер телефона:")

    async def complete(self, message: types.Message, state: FSMContext):
        """Завершение регистрации."""
        await state.set_state(RegistrationDialog.registration_complete)
        await message.reply("Регистрация завершена. Теперь вы можете использовать команды бота.")
# End-of-file (EOF)
