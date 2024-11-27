class MenuItem:
    def __init__(self, name, category, price, ingredients, size=None, temperature=None, isAlcoholic=None):
        self.name = name
        self.category = category
        self.price = price
        self.ingredients = ingredients
        self.size = size
        self.temperature = temperature
        self.isAlcoholic = isAlcoholic

    def get_description(self):
        """Returns a description of the item."""
        description = f"Name: {self.name}, Category: {self.category}, Ingredients: {', '.join(self.ingredients or [])}"
        if self.size:
            description += f", Size: {self.size}"
        if self.temperature:
            description += f", Temperature: {self.temperature}"
        if self.isAlcoholic is not None:
            description += f", Alcoholic: {'Yes' if self.isAlcoholic else 'No'}"
        return description

    def calculate_final_price(self, discount):
        """Calculates the price after a discount."""
        if 0 <= discount <= 100:
            return self.price * (1 - discount / 100)
        else:
            raise ValueError("Discount must be between 0 and 100")
