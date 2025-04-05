import asyncio
import logging as log

from aiogram import Bot, Dispatcher
from aiogram import types as aiogram_types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

from core.application.menu.config import MenuConfig
from core.config.config import ConfigManager, get_config as get_config
from core.infrastructure.config_reader import get_config as get_yaml_config
from modules.catalog.application.services.product_service import ProductService
from modules.catalog.domain.services.product_management_service import \
    ProductManagementService
from modules.catalog.infrastructure.database.category_repository_impl import \
    CategoryRepositoryImpl
from modules.catalog.infrastructure.database.product_fake_repository_impl import \
    ProductFakeRepositoryImpl
from modules.catalog.infrastructure.telegram_bot.handlers import \
    CatalogBotHandler
from modules.user.infrastructure.telegram_bot.handlers import StartHandler

# TODO: Add logging configuration from Config below
log.basicConfig(
    level=log.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ENTRY POINT
async def setup():

    # yaml_config = get_yaml_config()
    # config = get_config()

    config = ConfigManager.instance().config
    log.info(f"Customer telegram bot token: {config.customer_telegram_bot.token}")
    log.info(f"Admin telegram bot token: {config.admin_telegram_bot.token}")
    # log.info(f"Storage type: {config.storage.storage_type}")

    if config.customer_telegram_bot.token is None:
        log.error("Customer telegram bot token is not set.")
        return
    if config.admin_telegram_bot.token is None:
        log.error("Admin telegram bot token is not set.")
        return
        
    bot = Bot(token=config.customer_telegram_bot.token)
    dp = Dispatcher()
    # dp.storage = MemoryStorage()

    # TODO: Check: Probably it can be added into forms/views
    menu_config = MenuConfig()
    commands = menu_config.start().get_commands()
    await bot.set_my_commands(commands)

    set_customer_bot_dependences(bot, dp)

    await dp.start_polling(bot, skip_updates=True)

def set_customer_bot_dependences(bot:Bot, disp:Dispatcher) -> None:
 
    product_repository = ProductFakeRepositoryImpl()
    category_repository = CategoryRepositoryImpl()

    product_management_service = ProductManagementService(product_repository, category_repository)

    product_service = ProductService(product_repository, product_management_service)

    StartHandler(bot)\
        .register_hadlers(disp)

    CatalogBotHandler(product_service)\
        .register_handlers(disp)


if __name__ == '__main__':
    asyncio.run(setup())


