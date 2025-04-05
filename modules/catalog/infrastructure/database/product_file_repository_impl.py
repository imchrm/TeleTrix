from logging import log
from core.config.config import Config, ConfigManager
from modules.catalog.application.dtos.category_dto import CategoryDTO
from modules.catalog.domain.entities.product import Product
from modules.catalog.domain.repositories.product_repository import ProductRepository
from modules.catalog.infrastructure.file.structure import ProductStructure


class ProductFakeRepositoryImpl(ProductRepository):
    def save(self, product: Product):
        # Logic of saving to the database
        pass
    
    def get_by_id(self, id):
        raise NotImplementedError

    def get_all_products(self) -> list[Product]:
        # Logic of getting a list of all products from the database
        log.info('Getting all products from database...')
        config = config = ConfigManager.instance().config
        config.storage.storage_type
        ProductStructure.load_products()
        pass

    def delete(self, product: Product):
        raise NotImplementedError
    
    def find_by_category(self, category:CategoryDTO) -> list[Product]:
        products = []
