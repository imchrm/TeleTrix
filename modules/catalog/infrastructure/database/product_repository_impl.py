from asyncio import log
from modules.catalog.domain.repositories.product_repository import ProductRepository
from modules.catalog.domain.entities.product import Product


class ProductRepositoryImpl(ProductRepository):
    def save(self, product: Product):
        # Логика сохранения в БД
        pass

    def get_all_products(self):
        # Логика получения списка всех товаров из БД
        log.info('Getting all products from database...')
        pass

    def find_by_category(self, category):
            products = []
            for product in self.db.values():
                if product.category == category:
                    products.append(product)
            return products

def get_fake_product_list() -> list[Product]:
    """
    This handler prints a list of products.
    Each product has a photo, a description, and a quantity.
    """
    # Define a list of products as dictionaries.
    products = [
        {
            "photo": "https://images.uzum.uz/cpc7ptvfrr82f0a4na10/original.jpg",  # or use a file_id if already uploaded to Telegram
            "description": "Product 1: Amazing gadget with many features.",
            "quantity": 10
        },
        {
            "photo": "https://images.uzum.uz/cpc7ptvfrr82f0a4na10/original.jpg",
            "description": "Product 2: Innovative tool for daily tasks.",
            "quantity": 5
        },
        {
            "photo": "https://images.uzum.uz/cpc7ptvfrr82f0a4na10/original.jpg",
            "description": "Product 3: High-quality item for professionals.",
            "quantity": 8
        }
    ]
    
    # Send a separate photo message for each product.
    for product in products:
        caption = f"{product['description']}\nQuantity: {product['quantity']}"
        log.info(f"Sending product: {caption}")
       
