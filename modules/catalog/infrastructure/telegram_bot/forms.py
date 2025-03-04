from aiogram import types as aiogram_types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

class CategoryFilter(StatesGroup):
    waiting_for_category = State()

async def products_command(message: aiogram_types.Message, state: FSMContext):
    await CategoryFilter.waiting_for_category.set()

async def category_chosen(message: aiogram_types.Message, state: FSMContext):
    await state.finish()

def register_handlers_catalog(dp: Dispatcher):
    """ Interface """
    dp.register_message_handler(products_command, Command("products"))
    dp.register_message_handler(category_chosen, state=CategoryFilter.waiting_for_category)
