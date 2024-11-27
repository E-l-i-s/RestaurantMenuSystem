import pandas as pd

# Load the menu data from the CSV file
def load_menu(file_path):
    return pd.read_csv(file_path)

# Show the available categories
def show_categories(menu_data):
    """
    Display available categories from the menu.
    """
    categories = menu_data['Category'].unique()
    print("Available Categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    return categories

# Show items within a selected category
def show_items_in_category(menu_data, category):
    """
    Display items within a selected category and allow the user to choose.
    """
    # Filter items by the selected category
    category_items = menu_data[menu_data['Category'] == category]
    
    if category_items.empty:
        print("No items available in this category!")
        return None

    print(f"Items in {category}:")
    for i, row in category_items.iterrows():
        print(f"{i + 1}. {row['Name']} (Size: {row['Size'] if not pd.isna(row['Size']) else 'N/A'}, Price: ${row['Price']:.2f})")

    # Let user select an item by its index
    try:
        item_selection = int(input("Select an item by number: "))
        # Validate if the selection is within bounds
        if 1 <= item_selection <= len(category_items):
            selected_item = category_items.iloc[item_selection - 1]
            print(f"You selected: {selected_item['Name']}, priced at ${selected_item['Price']:.2f}")
            return selected_item
        else:
            print("Invalid item selection!")
            return None
    except ValueError:
        print("Please enter a valid number!")
        return None

# Main function to drive the program
def main():
    # Load the menu from the CSV
    file_path = 'path_to_your_csv_file.csv'  # Change to your actual file path
    menu_data = load_menu(file_path)

    # Show available categories
    categories = show_categories(menu_data)

    # Ask user to choose a category
    try:
        category_selection = int(input("Select a category by number: "))
        if 1 <= category_selection <= len(categories):
            selected_category = categories[category_selection - 1]
            # Show items in the selected category
            selected_item = show_items_in_category(menu_data, selected_category)
        else:
            print("Invalid category selection!")
    except ValueError:
        print("Please enter a valid number!")

if __name__ == "__main__":
    main()
