import pandas as pd
from menu_item import MenuItem

# Load the menu from the CSV file
def load_menu(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print("Error: The menu file was not found. Ensure the CSV file is in the same directory.")
        exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit()

# Display categories
def show_categories(menu_data):
    categories = menu_data["Category"].unique()
    print("\nAvailable Categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    return categories

# Display items in a selected category
def show_items_in_category(menu_data, category):
    print(f"\nItems in {category}:")
    items = menu_data[menu_data["Category"] == category]
    for i, row in items.iterrows():
        print(f"{i + 1}. {row['Name']} (Size: {row['size']}, Price: ${row['Price']:.2f})")
    return items

# Main program
def main():
    file_path = "ORdering system  - Sheet1.csv"  # Ensure the CSV file is in the same directory
    menu_data = load_menu(file_path)

    while True:
        print("\nWelcome to the Restaurant Menu System!")
        print("1. View Categories")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            categories = show_categories(menu_data)
            try:
                category_choice = int(input("\nSelect a category by number: ")) - 1
                if 0 <= category_choice < len(categories):
                    selected_category = categories[category_choice]
                    items_in_category = show_items_in_category(menu_data, selected_category)

                    # Allow user to select an item within the category
                    try:
                        item_choice = int(input("\nSelect an item by number: ")) - 1
                        if 0 <= item_choice < len(items_in_category):
                            selected_item = items_in_category.iloc[item_choice]
                            item_obj = MenuItem(
                                name=selected_item["Name"],
                                category=selected_item["Category"],
                                price=selected_item["Price"],
                                size=selected_item["size"],
                            )
                            print(f"\nYou selected: {item_obj.get_description()}")
                        else:
                            print("Invalid item selection!")
                    except ValueError:
                        print("Please enter a valid number.")
                else:
                    print("Invalid category selection!")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "2":
            print("Thank you for visiting. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

# Run the program
if __name__ == "__main__":
    main()
