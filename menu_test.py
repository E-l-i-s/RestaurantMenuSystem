import pandas as pd
import re  # For validating email addresses
from datetime import datetime
import os
from utils import load_menu, load_stop_list, save_to_csv, save_order_to_csv

def load_menu(file_path):
    """ 
    Loads menu data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: The menu data, or an empty DataFrame if an error occurs.
    """
    try:
        menu_data = pd.read_csv(file_path)
        menu_data.columns = menu_data.columns.str.strip()  # Clean column names
        return menu_data
    except FileNotFoundError:
        print(f"Error: The menu file could not be found at {file_path}. Please check the file path.")
        return pd.DataFrame()  # Return empty DataFrame in case of error
    except Exception as e:
        print(f"Unexpected error loading menu: {e}")
        return pd.DataFrame()


def load_stop_list(file_path):
    """ 
    Loads a list of out-of-stock items from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        list: List of out-of-stock item names, or an empty list if an error occurs.
    """
    try:
        stop_list = pd.read_csv(file_path)
        stop_list.columns = stop_list.columns.str.strip()  # Clean column names
        if 'Name' not in stop_list.columns:
            print(f"Error: The stop list CSV file does not contain expected column ('Name').")
            return []
        stop_list_names = stop_list['Name'].str.strip().tolist()  # Get list of out-of-stock item names
        return stop_list_names
    except FileNotFoundError:
        print(f"Error: The stop list file could not be found at {file_path}. Please check the file path.")
        return []  # Return empty list in case of error
    except Exception as e:
        print(f"Unexpected error loading stop list: {e}")
        return []


def show_categories(menu_data):
    """ 
    Display unique categories from a menu data dataframe.
    
    Args:
        menu_data (pd.DataFrame): A pandas dataframe containing a 'Category' column.
    
    Returns:
        np.ndarray: A list of unique category names as a numpy array.
    """
    categories = menu_data['Category'].unique()
    print("Available Categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    return categories


def show_items_in_category(menu_data, selected_category, stop_list):
    """ 
    Displays items from the selected category with their sizes, prices, and stock status.
    
    Args:
        menu_data (pd.DataFrame): DataFrame with 'Category', 'Name', 'Size', and 'Price'.
        selected_category (str): Category to display items from.
        stop_list (list): List of out-of-stock items.
    
    Returns:
        pd.DataFrame: Items in the selected category.
    """
    items_in_category = menu_data[menu_data['Category'] == selected_category]
    print(f"\nItems in {selected_category}:")
    index = 1
    for i, row in items_in_category.iterrows():
        item_name = row['Name']
        # Check if item is out of stock
        if item_name in stop_list:
            print(f"{index}. {item_name} (Out of Stock)")
        else:
            print(f"{index}. {item_name} (Size: {row['Size'] if pd.notna(row['Size']) else 'N/A'}, Price: ${row['Price']:.2f})")
        index += 1
    return items_in_category


def ask_payment_method(total_amount):
    """
    Ask the user for their payment method after the total amount is calculated.
    
    Args:
        total_amount (float): The total amount to be paid.
    
    Returns:
        str: Payment method ('Card' or 'Cash').
    """
    print(f"\nYour total amount is: ${total_amount:.2f}")
    while True:
        payment_method = input("How would you like to pay? (Card/Cash): ").strip().lower()
        if payment_method in ['card', 'cash']:
            return payment_method
        else:
            print("Invalid input. Please enter 'Card' or 'Cash'.")


def ask_email():
    """
    Ask the user for their email address. Ensures it's a valid email format.
    
    Returns:
        str: Validated email address.
    """
    while True:
        email = input("Please enter your email address: ").strip()
        # Regular expression for basic email validation
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_regex, email):
            return email
        else:
            print("Invalid email address. Please enter a valid email.")


def ask_dining_option():
    """
    Ask the user whether they want to dine in or take the food to go.
    
    Returns:
        str: "Dine In" or "Takeaway" based on user's choice.
    """
    while True:
        dining_option = input("Would you like to dine in or take the food to go? (Dine In/Takeaway): ").strip().lower()
        if dining_option in ['dine in', 'takeaway']:
            return dining_option.capitalize()
        else:
            print("Invalid input. Please enter 'Dine In' or 'Takeaway'.")


def main():
    """
    Main function for the ordering system. It loads the menu and stop list,
    displays categories and items, allows the user to place an order, and calculates
    the total price. The program continues until the user chooses to finish their order.
    """
    menu_file = 'ORdering system  - Sheet1.csv'  # Correct menu CSV file name
    stop_list_file = 'stop_list_for_the_ordering_system.csv'  # Correct stop list CSV file name
    order_file = 'orders.csv'  # CSV file to store orders

    # Load menu data and stop list
    menu_data = load_menu(menu_file)
    stop_list = load_stop_list(stop_list_file)

    if menu_data.empty or not stop_list:
        print("Error: No menu or stop list data found. Exiting program.")
        return

    # Ask user for dining option (Dine In or Takeaway)
    dining_option = ask_dining_option()
    print(f"\nYou chose to {dining_option}.")

    total_price = 0
    while True:
        # Show available categories
        categories = show_categories(menu_data)

        # User selects a category
        try:
            selected_category_index = int(input("\nSelect a category by number: ")) - 1
            selected_category = categories[selected_category_index]
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid category number.")
            continue

        # Show items in the selected category
        items_in_category = show_items_in_category(menu_data, selected_category, stop_list)

        # User selects an item
        try:
            selected_item_index = int(input("\nSelect an item by number: ")) - 1
            selected_item = items_in_category.iloc[selected_item_index]
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid item number.")
            continue

        item_name = selected_item['Name']
        if item_name in stop_list:
            print(f"Oops! We are out of stock for '{item_name}'. Please choose another item.")
            continue

        # Add price of selected item to total
        total_price += selected_item['Price']

        # Save order to CSV
        order_data = {
            'Item Name': item_name,
            'Size': selected_item['Size'] if pd.notna(selected_item['Size']) else 'N/A',
            'Price': selected_item['Price'],
            'Dining Option': dining_option
        }
        save_order_to_csv(order_data, order_file)

        # Ask if the user wants to order more
        while True:
            more_order = input("Is there anything else you want to order? (Yes/No): ").strip().lower()
            if more_order == 'yes':
                break
            elif more_order == 'no':
                # After finalizing the order, ask for payment method
                payment_method = ask_payment_method(total_price)

                # Ask for user's email
                email = ask_email()

                # Show order confirmation
                print(f"Thank you for your order! You chose to pay by {payment_method.capitalize()}.")
                print(f"A receipt will be sent to {email}.")
                print(f"Your order is ready for {dining_option.lower()}.")
                return
            else:
                print("Please answer with 'Yes' or 'No' only.")

if __name__ == "__main__":
    main()
