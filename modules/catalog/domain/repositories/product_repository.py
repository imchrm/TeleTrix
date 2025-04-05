# Interface or abstract class for ProductRepositoryImpl
from abc import abstractmethod
from core.domain.repositories.repository import Repository
from modules.catalog.domain.entities.product import Product

@abstractmethod
class ProductRepository(Repository):
    @abstractmethod
    def save(self, product: Product):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id):
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, product: Product):
        raise NotImplementedError

    @abstractmethod
    def get_all_products(self):
        raise NotImplementedError

    @abstractmethod
    def find_by_category(self, category) -> list[Product]:
        pass