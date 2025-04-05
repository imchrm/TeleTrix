import logging as log
from typing_extensions import override
from modules.catalog.application.dtos.category_dto import CategoryDTO
from modules.catalog.domain.entities.category import Category
from modules.catalog.domain.repositories.product_repository import ProductRepository
from modules.catalog.domain.entities.product import Product


class ProductFakeRepositoryImpl(ProductRepository):
    db = {}
    def save(self, product: Product):
        # Логика сохранения в БД
        pass

    def get_all_products(self) -> list[Product] | None:
        # Логика получения списка всех товаров из БД
        log.info('Getting all products from database...')
        return None

    @override
    def find_by_category(self, category:CategoryDTO) -> list[Product]:
        products = []
        # TODO: Make a global test mode configuration
        PRODUCTION = False
        if PRODUCTION:
            for product in self.db.values():
                if product.category == category:
                    products.append(product)
            # return products
        else: #Test mode
            products_dict = self.get_fake_product_list()
            products = [
            Product(
                id=p.get('id', 0),
                name=p.get('name', "Unknown"),
                description=p.get('description', "undefined"),
                price=p.get('price', 0.00),
                photo=p.get('image_url', "https://images.uzum.uz/cpc7ptvfrr82f0a4na10/original.jpg"),
                quantity=p.get('quantity', 0),
                category=Category(value=p.get('category_id', "#0000"), description=p.get('category', 'Nothing'))
            ) for p in products_dict
]
        return products

    def get_fake_product_list(self) -> list[dict]:
        """
        This handler prints a list of products.
        Each product has a photo, a description, and a quantity.
        """
        # Define a list of products as dictionaries.
        products = [
            {
                "name": "Product 1",
                "photo": "https://images.uzum.uz/cpc7ptvfrr82f0a4na10/original.jpg",  # or use a file_id if already uploaded to Telegram
                "description": "Product 1: Amazing gadget with many features.",
                "quantity": 10,
                "price": 100,
            },
            {
                "name": "Product 2",
                "photo": "https://images.uzum.uz/cpc7ptvfrr82f0a4na10/original.jpg",
                "description": "Product 2: Innovative tool for daily tasks.",
                "quantity": 5,
                "price": 200,
            },
            {   
                "name": "Product 3",
                "photo": "https://images.uzum.uz/cpc7ptvfrr82f0a4na10/original.jpg",
                "description": "Product 3: High-quality item for professionals.",
                "quantity": 8,
                "price": 150,
            }
        ]

        # Send a separate photo message for each product.
        for product in products:
            caption = f"{product['description']}\nQuantity: {product['quantity']}"
            log.info("Sending product: %s ", caption)

        return products
    
    def get_by_id(self, id):
        # Логика получения товара по ID из БД
        pass
    
    def delete(self, product: Product):
        # Логика удаления товара из БД
        pass
        
