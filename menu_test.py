import pandas as pd
from menu_item import MenuItem

# Load the menu from the CSV file
def load_menu(file_path):
    data = pd.read_csv(file_path)
    return data

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
        print(f"- {row['Name']} (Size: {row['size']}, Price: ${row['Price']:.2f})")

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
            category_choice = int(input("\nSelect a category by number: ")) - 1
            
            if 0 <= category_choice < len(categories):
                selected_category = categories[category_choice]
                show_items_in_category(menu_data, selected_category)
            else:
                print("Invalid category selection!")
        elif choice == "2":
            print("Thank you for visiting. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

# Run the program
if __name__ == "__main__":
    main()
