import pandas as pd

class StockManager:
    """
    Manages stock for items in a menu.
    Includes functionality for loading, checking, and updating stock levels.
    """

    def __init__(self, menu_file):
        """
        Initialize the StockManager with a menu file.

        Args:
            menu_file (str): Path to the menu CSV file.
        """
        self.menu_file = menu_file
        self.menu_data = pd.read_csv(menu_file)

    def is_item_available(self, item_name, quantity):
        """
        Check if an item is available in the required quantity.

        Args:
            item_name (str): Name of the item.
            quantity (int): Quantity requested.

        Returns:
            bool: True if the item is available, False otherwise.
        """
        item = self.menu_data[self.menu_data['Name'] == item_name]
        if not item.empty:
            available_quantity = item.iloc[0]['Stock']
            return available_quantity >= quantity
        return False

    def update_stock(self, item_name, quantity):
        """
        Update the stock for an item after it has been ordered.

        Args:
            item_name (str): Name of the item.
            quantity (int): Quantity to deduct.

        Returns:
            None
        """
        item_index = self.menu_data[self.menu_data['Name'] == item_name].index
        if not item_index.empty:
            self.menu_data.at[item_index[0], 'Stock'] -= quantity

    def save_updated_menu(self):
        """
        Save the updated menu data back to the CSV file.

        Returns:
            None
        """
        self.menu_data.to_csv(self.menu_file, index=False)


class Order(StockManager):
    """
    Represents a customer order, encapsulating item selections, quantities, and total price.
    Inherits stock management functionality from StockManager.
    """

    def __init__(self, menu_file):
        """
        Initialize an empty order and inherit StockManager functionalities.
        
        Args:
            menu_file (str): Path to the menu CSV file.
        """
        super().__init__(menu_file)
        self.items = []
        self.total_price = 0

    def add_item(self, item_name, price, quantity):
        """
        Add an item to the order if it's available in stock.

        Args:
            item_name (str): Name of the item.
            price (float): Price of the item.
            quantity (int): Quantity ordered.

        Returns:
            None
        """
        if self.is_item_available(item_name, quantity):
            self.items.append({'Item': item_name, 'Price': price, 'Quantity': quantity})
            self.total_price += price * quantity
            self.update_stock(item_name, quantity)
            print(f"Added {quantity} x {item_name} to your order.")
        else:
            print(f"Sorry, {item_name} is not available in the requested quantity.")

