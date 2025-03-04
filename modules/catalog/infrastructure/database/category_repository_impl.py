from asyncio import log
from modules.catalog.domain.repositories.category_repository import CategoryRepository
from modules.catalog.domain.entities import product


class CategoryRepositoryImpl(CategoryRepository):
    def save(self, product: product):
        # Логика сохранения в БД
        super().save(product)

    def get_by_id(self, id):
        # Логика получения категории по id из БД
        log.info('Getting all products from database...')
        try:
            return super().get_by_id(id)
        except Exception as e:
            log.error(f"Error in get_by_id: {e}")
            raise

    def get_all_products(self):
        # Логика получения списка всех товаров из БД
        log.info('Getting all products from database...')
    
    def find_by_category(self, category):
            products = []
            for product in self.db.values():
                if product.category == category:
                    products.append(product)
            return products