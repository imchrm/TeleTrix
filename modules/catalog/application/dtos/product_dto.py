

class ProductDTO():
    def __init__(self, id=None, name="", price=0.0, description="", category=""):
        super().__init__(id)
        self.name = name
        self.price = price
        self.description = description
        self.category = category

    def set_name(self, name):
        self.name = name
        return self

    def set_price(self, price):
        self.price = price
        return self

    def set_description(self, description):
        self.description = description
        return self

    def set_category(self, category):
        self.category = category
        return self

    def __repr__(self):
        return (f"ProductDTO(id={self.id}, name={self.name}, price={self.price}, "
                f"description={self.description}, category={self.category})")