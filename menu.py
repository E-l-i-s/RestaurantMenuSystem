import pandas as pd

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
        return f"{self.name} ({self.category}): {', '.join(self.ingredients) if self.ingredients else 'No ingredients specified'}"

    def calculate_final_price(self, discount=0):
        return self.price * (1 - discount)

class Salad(MenuItem):
    def __init__(self, name, price, ingredients):
        super().__init__(name, "Salad", price, ingredients)

class Drink(MenuItem):
    def __init__(self, name, price, isAlcoholic, temperature):
        super().__init__(name, "Drink", price, None, None, temperature, isAlcoholic)

def load_menu(file_path):
    menu_data = pd.read_csv(file_path)
    menu_data.columns = menu_data.columns.str.strip()  # Ensure no extra spaces in column names
    return menu_data