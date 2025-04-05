from modules.catalog.application.dtos.product_dto import ProductDTO
from modules.catalog.domain.repositories.product_repository import ProductRepository
from modules.catalog.domain.entities.product import Product
from modules.catalog.domain.services.product_management_service import ProductManagementService


class ProductService:
    def __init__(self, product_repository: ProductRepository, product_management_service: ProductManagementService):
        self.product_repository = product_repository
        self.product_management_service = product_management_service

    def add_product(self, product_data: dict):
        """ Создает новый товар """
        # Validation of data
        # TODO: validate_product_data(product_data)
        product_instance = Product(**product_data)
        self.product_management_service.create_product(product_instance)
        self.product_repository.save(product_instance)

    def get_all_products(self):
        # Return of pool of all products like the list of ProductDTO
        return self.product_repository.get_all_products()

    def get_products_by_category(self, category) -> list[Product]:
        self.product_management_service
        return self.product_repository.find_by_category(category)

    def get_product_dto(self, product_id):
        """ Example of DTO """
        product = self.product_repository.get_by_id(product_id)
        # Преобразует Product в ProductDTO
        product_dto = ProductDTO(product.name, product.price, ...)
        return product_dto

