import asyncio
import os
import logging as log

from aiogram import Bot, Dispatcher
from aiogram import types as aiogram_types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import bold

from modules.catalog.application.services.product_service import ProductService
from modules.catalog.domain.services.product_management_service import \
    ProductManagementService
from modules.catalog.infrastructure.database.category_repository_impl import \
    CategoryRepositoryImpl
from modules.catalog.infrastructure.database.product_repository_impl import \
    ProductRepositoryImpl
from modules.catalog.infrastructure.telegram_bot.handlers import \
    CatalogBotHandler

import sqlite3
from core.config.config import get_config as get_config
from core.infrastructure.config_reader import get_config as get_yaml_config
from dotenv import load_dotenv

log.basicConfig(
    level=log.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
bot = Bot(token='7819586592:AAHRXzbVvKG9AiiueCLkG92BcCr_PS7P6rc')
dp = Dispatcher()

product_repository = ProductRepositoryImpl()
category_repository = CategoryRepositoryImpl()

product_management_service = ProductManagementService(product_repository, category_repository)

product_service = ProductService(product_repository, product_management_service)

catalog_handler = CatalogBotHandler(product_service)
catalog_handler.register_handlers(dp)

# ENTRY POINT
async def setup():

    # yaml_config = get_yaml_config()

    config = get_config()
    log.info(f"TELEGRAM_BOT_TOKEN: {config.telegram_bot.token}")

    # db_config = config['database']
    # DATABASE_URL = f"{db_config['engine']}://{db_config['user']}:{os.environ.get('DB_PASSWORD', '')}@{db_config['host']}:{db_config['port']}/{db_config['name']}"
    # logging.info(f"Database URL: {DATABASE_URL}")
    

    await set_bot_commands()
    await dp.start_polling(bot, skip_updates=True)

async def set_bot_commands() -> None:
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
    await message.answer(f"Hello, {bold(message.from_user.full_name)}!")


if __name__ == '__main__':
    asyncio.run(setup())


