# Interface or abstract class for ProductRepositoryImpl
from abc import abstractmethod
from core.domain.repositories.repository import Repository
from modules.catalog.domain.entities import product


class ProductRepository(Repository):
    def save(self, product: product):
        raise NotImplementedError
    
    def get_by_id(self, id):
        raise NotImplementedError
    
    def delete(self, product: product):
        raise NotImplementedError

    def get_all_products(self):
        raise NotImplementedError

    @abstractmethod
    def find_by_category(self, category):
        pass