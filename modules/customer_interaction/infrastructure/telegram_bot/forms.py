from aiogram.dispatcher import FSMContext
from aiogram import types as aiogram_types
from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    name = State()
    age = State()

async def start_registration(message: aiogram_types.Message, state: FSMContext):
    await Registration.name.set()
    await message.reply("Введите ваше имя:")

async def process_name(message: aiogram_types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Registration.next()
    await message.reply("Введите ваш возраст:")

async def process_age(message: aiogram_types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
        name = data['name']
        age = data['age']
    await state.finish()
    await message.reply(f"Ваше имя: {name}, возраст: {age}")
