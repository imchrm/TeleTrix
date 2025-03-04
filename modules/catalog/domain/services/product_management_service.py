import asyncio
import logging as log

from modules.catalog.domain.repositories.product_repository import ProductRepository

class ProductManagementService:
        def __init__(self, product_repository:ProductRepository, category_repository):
            self.product_repository = product_repository
            self.category_repository = category_repository

        def create_product(self, product):
            """Создает новый товар, проверяя наличие категории."""

            category = self.category_repository.get_by_id(product.category.id)
            if not category:
                raise ValueError(f"Category with id {product.category.id} does not exist.")

            # TODO: Дополнительные проверки (например, уникальность названия) можно добавить здесь.

            return self.product_repository.save(product)

        async def update_product_price(self, product_id, new_price):
            """Обновляет цену товара, проверяя допустимый диапазон."""

            product = await self.product_repository.get_by_id(product_id)
            if not product:
                raise ValueError(f"Product with id {product_id} does not exist.")

            if new_price <= 0:
                raise ValueError("Price must be positive.")

            product.price = new_price
            return self.product_repository.save(product)

        async def assign_category_to_product(self, product_id, category_id):
            """Назначает категорию товару, проверяя существование категории."""

            product = await self.product_repository.get_by_id(product_id)
            if not product:
                raise ValueError(f"Product with id {product_id} does not exist.")

            category = self.category_repository.get_by_id(category_id)
            if not category:
                raise ValueError(f"Category with id {category_id} does not exist.")

            product.category = category
            return self.product_repository.save(product)

        # Другие методы для реализации сложной бизнес-логики...