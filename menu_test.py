from menu import load_menu
import pandas as pd

def show_categories(menu_data):
    """Display available categories to the user."""
    categories = menu_data['Category'].unique()
    print("\nAvailable Categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    return categories

def show_items_in_category(menu_data, selected_category):
    """Display items in the selected category."""
    items_in_category = menu_data[menu_data['Category'] == selected_category].reset_index(drop=True)
    print(f"\nItems in {selected_category}:")
    for i, row in items_in_category.iterrows():
        print(f"{i + 1}. {row['Name']} (Price: ${row['Price']:.2f})")
    return items_in_category

def get_valid_input(prompt, valid_range):
    """Prompt the user for input and validate it."""
    while True:
        try:
            user_input = int(input(prompt))
            if 1 <= user_input <= valid_range:
                return user_input
            else:
                print(f"Please enter a number between 1 and {valid_range}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():
    # Load menu data
    try:
        menu_data = load_menu('ORdering system  - Sheet1.csv')  # Ensure the correct CSV path
    except FileNotFoundError:
        print("Error: The menu file could not be found. Please check the file path.")
        return
    except Exception as e:
        print(f"Unexpected error loading menu: {e}")
        return

    # Initialize total and order details
    final_price = 0.0
    order_details = []

    while True:
        # Show available categories
        categories = show_categories(menu_data)

        # User selects a category
        selected_category_index = get_valid_input("\nSelect a category by number: ", len(categories))
        selected_category = categories[selected_category_index - 1]

        # Show items in the selected category
        items_in_category = show_items_in_category(menu_data, selected_category)

        # User selects an item
        selected_item_index = get_valid_input("\nSelect an item by number: ", len(items_in_category))
        selected_item = items_in_category.iloc[selected_item_index - 1]

        # Add to final price and order details
        item_name = selected_item['Name']
        item_price = selected_item['Price']
        final_price += item_price
        order_details.append(f"{item_name} (${item_price:.2f})")

        print(f"\nYou selected: {item_name}")
        print(f"Price: ${item_price:.2f}")
        print(f"Current total: ${final_price:.2f}")

        # Ask if the user wants to continue ordering
        while True:
            more_order = input("\nWould you like to order anything else? (yes/no): ").strip().lower()
            if more_order == 'yes' or more_order == 'no':
                break
            print("Invalid input. Please answer with 'yes' or 'no' only. Choose if you want to order something more or finish your order.")

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
