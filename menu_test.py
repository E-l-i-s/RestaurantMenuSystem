from menu import load_menu
import pandas as pd

def show_categories(menu_data):
    categories = menu_data['Category'].unique()
    print("Available Categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    return categories

def show_items_in_category(menu_data, selected_category):
    items_in_category = menu_data[menu_data['Category'] == selected_category]
    print(f"\nItems in {selected_category}:")
    for i, row in items_in_category.iterrows():
        print(f"{i + 1}. {row['Name']} (Size: {row['Size'] if pd.notna(row['Size']) else 'N/A'}, Price: ${row['Price']:.2f})")
    return items_in_category

def main():
    # Load menu data
    menu_data = load_menu('ORdering system  - Sheet1.csv')  # Ensure the correct CSV path is here

    # Show available categories
    categories = show_categories(menu_data)

    # User selects a category
    selected_category_index = int(input("\nSelect a category by number: ")) - 1
    selected_category = categories[selected_category_index]

    # Show items in the selected category
    items_in_category = show_items_in_category(menu_data, selected_category)

    # User selects an item
    selected_item_index = int(input("\nSelect an item by number: ")) - 1
    selected_item = items_in_category.iloc[selected_item_index]

    print(f"\nYou selected: {selected_item['Name']}")
    print(f"Price: ${selected_item['Price']:.2f}")
    print(f"Description: {selected_item['Name']} ({selected_category}): {selected_item['Ingredients'] if pd.notna(selected_item['Ingredients']) else 'No ingredients specified'}")

if __name__ == "__main__":
    main()