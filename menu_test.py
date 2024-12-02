from menu import load_menu
import pandas as pd

def show_categories(menu_data):
    categories = menu_data['Category'].unique()
    print("Available Categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    return categories

def show_items_in_category(menu_data, selected_category):
    items_in_category = menu_data[menu_data['Category'] == selected_category].reset_index(drop=True)
    print(f"\nItems in {selected_category}:")
    for i, row in items_in_category.iterrows():
        print(f"{i + 1}. {row['Name']} (Price: ${row['Price']:.2f})")
    return items_in_category

def main():
    # Load menu data
    menu_data = load_menu('ORdering system  - Sheet1.csv')  # Ensure the correct CSV path is here

    final_price = 0.0
    order_details = []

    while True:
        # Show available categories
        categories = show_categories(menu_data)

        # User selects a category
        try:
            selected_category_index = int(input("\nSelect a category by number: ")) - 1
            if selected_category_index < 0 or selected_category_index >= len(categories):
                raise ValueError("Invalid category selection.")
            selected_category = categories[selected_category_index]
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid category number.")
            continue

        # Show items in the selected category
        items_in_category = show_items_in_category(menu_data, selected_category)

        # User selects an item
        try:
            selected_item_index = int(input("\nSelect an item by number: ")) - 1
            if selected_item_index < 0 or selected_item_index >= len(items_in_category):
                raise ValueError("Invalid item selection.")
            selected_item = items_in_category.iloc[selected_item_index]
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid item number.")
            continue

        # Add to final price and order details
        item_name = selected_item['Name']
        item_price = selected_item['Price']
        final_price += item_price
        order_details.append(f"{item_name} (${item_price:.2f})")

        print(f"\nYou selected: {item_name}")
        print(f"Price: ${item_price:.2f}")
        print(f"Current total: ${final_price:.2f}")

        # Ask if user wants to continue ordering
        more_order = input("\nWould you like to order anything else? (yes/no): ").strip().lower()
        if more_order == 'no':
            break

    # Final order summary
    print("\nYour Order Summary:")
    for detail in order_details:
        print(f"- {detail}")
    print(f"Final Price: ${final_price:.2f}")
    print("Thank you for your order!")

if __name__ == "__main__":
    main()
