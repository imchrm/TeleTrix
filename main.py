import asyncio
import logging as log
import os
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram import types as aiogram_types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import bold
from dotenv import load_dotenv

from core.config.config import ConfigManager, get_config as get_config
from core.infrastructure.config_reader import get_config as get_yaml_config
from modules.catalog.application.services.product_service import ProductService
from modules.catalog.domain.services.product_management_service import \
    ProductManagementService
from modules.catalog.infrastructure.database.category_repository_impl import \
    CategoryRepositoryImpl
from modules.catalog.infrastructure.database.product_repository_impl import \
    ProductRepositoryImpl
from modules.catalog.infrastructure.telegram_bot.handlers import \
    CatalogBotHandler
from modules.user.infrastructure.telegram_bot.handlers import StartHandler

log.basicConfig(
    level=log.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ENTRY POINT
async def setup():

    # yaml_config = get_yaml_config()
    # config = get_config()

    config = ConfigManager.instance().config
    log.info(f"TELEGRAM_BOT_TOKEN: {config.telegram_bot.token}")

    bot = Bot(token=config.telegram_bot.token)
    dp = Dispatcher()
    dp.storage = MemoryStorage()

    set_app_independences(bot, dp)

    await set_bot_commands(bot)
    await dp.start_polling(bot, skip_updates=True)

def set_app_independences(bot:Bot, disp:Dispatcher) -> None:
 
    product_repository = ProductRepositoryImpl()
    category_repository = CategoryRepositoryImpl()

    product_management_service = ProductManagementService(product_repository, category_repository)

    product_service = ProductService(product_repository, product_management_service)

    start_hadler = StartHandler(bot)
    start_hadler.register_hadlers(disp)

    catalog_handler = CatalogBotHandler(product_service)
    catalog_handler.register_handlers(disp)

async def set_bot_commands(bot:Bot) -> None:
    commands = [
        aiogram_types.BotCommand(command="start", description="Start the bot"),
        aiogram_types.BotCommand(command="help", description="Show help information"),
        aiogram_types.BotCommand(command="list", description="List information"),
        aiogram_types.BotCommand(command="products", description="View available products")
    ]
    await bot.set_my_commands(commands)

@dp.message(CommandStart())
async def command_start_handler(message: aiogram_types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    chat_id = message.chat.id
    await message.answer(f"Bot ID: {bot.id}")
    await message.answer(f"Chat ID: {chat_id}")
    await message.answer(f"User ID: {bold(message.from_user.id)}")
    await message.answer(f"User name: {bold(message.from_user.full_name)}")


if __name__ == '__main__':
    asyncio.run(setup())


