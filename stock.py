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

class Order:
    """
    Represents a customer order, encapsulating item selections, quantities, and total price.
    """

    def __init__(self):
        """Initialize an empty order."""
        self.items = []
        self.total_price = 0

    def add_item(self, item_name, price, quantity):
        """
        Add an item to the order.

        Args:
            item_name (str): Name of the item.
            price (float): Price of the item.
            quantity (int): Quantity ordered.

        Returns:
            None
        """
        self.items.append({'Item': item_name, 'Price': price, 'Quantity': quantity})
        self.total_price += price * quantity

    def show_order_summary(self):
        """
        Display the order summary.

        Returns:
            None
        """
        print("\nOrder Summary:")
        for item in self.items:
            print(f"{item['Item']} (x{item['Quantity']}): ${item['Price'] * item['Quantity']:.2f}")
        print(f"Total Price: ${self.total_price:.2f}")

class User:
    """
    Represents a user, including their email and dining preferences.
    """

    def __init__(self, email=None, dining_option=None):
        """Initialize the user with optional email and dining preferences."""
        self.email = email
        self.dining_option = dining_option

    def set_email(self, email):
        """Set the user's email."""
        self.email = email

    def set_dining_option(self, option):
        """Set the user's dining option."""
        self.dining_option = option

    def get_user_details(self):
        """Return user details as a dictionary."""
        return {'Email': self.email, 'Dining Option': self.dining_option}

# Example usage of the improved OOP structure
if __name__ == "__main__":
    stock_manager = StockManager('menu.csv')
    user = User()
    order = Order()

    # Simulate setting user details
    user.set_email("test@example.com")
    user.set_dining_option("Dine In")

    # Simulate adding items to the order
    if stock_manager.is_item_available("Pizza", 2):
        order.add_item("Pizza", 10.99, 2)
        stock_manager.update_stock("Pizza", 2)

    # Save updated stock and show order summary
    stock_manager.save_updated_menu()
    order.show_order_summary()
    print(f"User Details: {user.get_user_details()}")
