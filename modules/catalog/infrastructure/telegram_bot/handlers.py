from modules.catalog.application.services.product_service import ProductService
from aiogram import Dispatcher, types as aiogram_types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command

from modules.catalog.infrastructure.telegram_bot.forms import CategoryFilter

class CatalogBotHandler:
    def __init__(self, product_service: ProductService):
        self.product_service = product_service

    async def handle_add_product_command(self, message: aiogram_types.Message, state: FSMContext):
        """ Отправка списка товаров пользователю через Telegram API """
        products = self.product_service.get_all_products()
        await message.answer(str(products))

    # async def handle_get_products_command(self, message: aiogram_types.Message, state: FSMContext):
        # """ Отправка списка товаров пользователю через Telegram API """
        # products = self.product_service.get_products()
        # await message.answer(str(products))

    async def products_command(self, message: aiogram_types.Message, state: FSMContext):
        """ Отправка списка товаров пользователю через Telegram API """
        await message.reply("Введите категорию товара:")
        await state.set_state(CategoryFilter.waiting_for_category)

    async def category_chosen(self, message: aiogram_types.Message, state: FSMContext):
        category = message.text
        # Получение товаров из сервиса с учетом категории
        products = self.product_service.get_products_by_category(category) #Предполагается что в сервисе есть такой метод
        
        if products:
            formatted_products = "\n".join([
                # f"{p.get('name', 'Unknown')} - ${p.get('price', 0):.2f}"
                f"{p.name} - ${p.price:.2f}"
                for p in products
            ])
            await message.reply(f"Товары в категории: {category}\n{formatted_products}")
        else:
            await message.reply(f"Товары в категории {category} не найдены.")

        await state.clear()

    def register_handlers(self, dp: Dispatcher):
        dp.message.register(self.products_command, Command("products"))
        dp.message.register(self.category_chosen, CategoryFilter.waiting_for_category)




