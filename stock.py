import pandas as pd

class StockManager:
    def __init__(self, menu_file):
        """Initialize the StockManager with the menu file."""
        self.menu_file = menu_file
        self.menu_data = self._load_menu()

    def _load_menu(self):
        """Load the menu data from the CSV file."""
        try:
            menu_data = pd.read_csv(self.menu_file)
            menu_data.columns = menu_data.columns.str.strip()  # Clean column names
            return menu_data
        except FileNotFoundError:
            print(f"Error: The menu file could not be found at {self.menu_file}.")
            return pd.DataFrame()
        except Exception as e:
            print(f"Unexpected error loading menu: {e}")
            return pd.DataFrame()

    def is_item_available(self, item_name, quantity):
        """Check if an item is available in the requested quantity."""
        item = self.menu_data[self.menu_data['Name'] == item_name]
        if item.empty:
            print(f"Error: Item '{item_name}' not found in the menu.")
            return False
        available_stock = item.iloc[0]['Stock']
        return available_stock >= quantity

    def update_stock(self, item_name, quantity):
        """Deduct the stock for an item after it's ordered."""
        index = self.menu_data[self.menu_data['Name'] == item_name].index
        if not index.empty:
            current_stock = self.menu_data.at[index[0], 'Stock']
            self.menu_data.at[index[0], 'Stock'] = max(0, current_stock - quantity)

    def save_updated_menu(self):
        """Save the updated menu data back to the CSV file."""
        try:
            self.menu_data.to_csv(self.menu_file, index=False)
        except Exception as e:
            print(f"Error saving updated menu: {e}")
