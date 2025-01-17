import pandas as pd
import re  # For validating email addresses
from stock import StockManager  # Import StockManager class
from utils import save_order_to_csv

def show_categories(menu_data):
    """Display unique categories from a menu data dataframe."""
    categories = menu_data['Category'].unique()
    print("Available Categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    return categories

def show_items_in_category(menu_data, selected_category):
    """
    Display items in the selected category, with numbering starting from 1.
    
    Args:
        menu_data (pd.DataFrame): The menu data.
        selected_category (str): The selected category.
    
    Returns:
        pd.DataFrame: The items in the selected category.
    """
    items_in_category = menu_data[menu_data['Category'] == selected_category]
    print(f"\nItems in {selected_category}:")
    for i, (_, row) in enumerate(items_in_category.iterrows(), start=1):
        item_name = row['Name']
        print(f"{i}. {item_name} (Size: {row['Size']}, Price: ${row['Price']:.2f})")
    return items_in_category

def ask_payment_method(total_amount):
    """Ask the user for their payment method and handle cash payments with change."""
    print(f"\nYour total amount is: ${total_amount:.2f}")
    while True:
        payment_method = input("How would you like to pay? (Card/Cash): ").strip().lower()
        if payment_method == 'card':
            return payment_method
        elif payment_method == 'cash':
            while True:
                try:
                    cash_amount = float(input("Enter the cash amount: $"))
                    if cash_amount >= total_amount:
                        change = cash_amount - total_amount
                        if change > 0:
                            print(f"Your change is ${change:.2f}. Thank you!")
                        else:
                            print("Thank you for your payment!")
                        return payment_method
                    else:
                        print(f"Insufficient amount. You owe ${total_amount - cash_amount:.2f}.")
                except ValueError:
                    print("Please enter a valid amount.")
        else:
            print("Invalid input. Please choose 'Card' or 'Cash'.")

def ask_email():
    """Ask the user for their email address and validate it."""
    while True:
        email = input("Enter your email address: ").strip()
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_regex, email):
            return email
        else:
            print("Invalid email format. Please try again.")

def ask_dining_option():
    """Ask the user if they want to dine in or take away."""
    while True:
        option = input("Would you like to dine in or takeaway? (Dine In/Takeaway): ").strip().lower()
        if option in ['dine in', 'takeaway']:
            return option.capitalize()
        else:
            print("Invalid choice. Please choose 'Dine In' or 'Takeaway'.")

def main():
    """Main function to handle the ordering process."""
    menu_file = 'ORdering system  - Sheet1.csv'  # Path to menu CSV
    order_file = 'orders.csv'  # Path to save orders

    # Initialize StockManager
    stock_manager = StockManager(menu_file)
    menu_data = stock_manager.menu_data

    # Ask for dining option
    dining_option = ask_dining_option()
    print(f"\nYou chose to {dining_option}.")

    total_price = 0
    ordered_items = []

    while True:
        # Show categories
        categories = show_categories(menu_data)

        # Choose a category
        try:
            selected_category_index = int(input("\nSelect a category by number: ")) - 1
            selected_category = categories[selected_category_index]
        except (ValueError, IndexError):
            print("Invalid choice. Please select a valid category.")
            continue

        # Show items in the chosen category
        items_in_category = show_items_in_category(menu_data, selected_category)

        # Choose an item
        try:
            selected_item_index = int(input("\nSelect an item by number: ")) - 1
            selected_item = items_in_category.iloc[selected_item_index]
        except (ValueError, IndexError):
            print("Invalid choice. Please select a valid item.")
            continue

        item_name = selected_item['Name']

        # Check stock
        while True:
            try:
                quantity = int(input(f"How many '{item_name}' would you like to order? "))
                if quantity <= 0:
                    print("Quantity must be at least 1.")
                elif not stock_manager.is_item_available(item_name, quantity):
                    print(f"Sorry, '{item_name}' is out of stock or insufficient quantity.")
                    break
                else:
                    # Update stock and save
                    stock_manager.update_stock(item_name, quantity)
                    stock_manager.save_updated_menu()

                    # Add to order
                    total_price += selected_item['Price'] * quantity
                    ordered_items.append(f"{item_name} (x{quantity})")

                    # Save order to CSV
                    order_data = {
                        'Item Name': item_name,
                        'Size': selected_item['Size'],
                        'Price': selected_item['Price'],
                        'Quantity': quantity,
                        'Dining Option': dining_option
                    }
                    save_order_to_csv(order_data, order_file)
                    break
            except ValueError:
                print("Please enter a valid number.")

        # Check if user wants to order more
        more_order = input("Would you like to order more? (Yes/No): ").strip().lower()
        if more_order == 'no':
            break

    # Show order summary and confirm
    print(f"\nYour order: {', '.join(ordered_items)}.")
    confirm = input("Would you like to confirm this order? (Yes/No): ").strip().lower()
    if confirm == 'yes':
        payment_method = ask_payment_method(total_price)
        email = ask_email()
        print(f"\nThank you! Your order is confirmed. A receipt will be sent to {email}.")
    else:
        print("Order canceled.")

if __name__ == "__main__":
    main()
