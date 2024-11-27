class MenuItem:
    def __init__(self, name, category, price, size=None):
        self.name = name
        self.category = category
        self.price = price
        self.size = size

    def get_description(self):
        """Returns a description of the item."""
        description = f"Name: {self.name}, Category: {self.category}, Size: {self.size}, Price: ${self.price:.2f}"
        return description
