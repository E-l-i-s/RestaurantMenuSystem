class Dish:
    def __init__(self, name, price):
        self.name = name  # Name of the dish
        self.price = price  # Price of the dish

    def __str__(self):
        return f"{self.name} - {self.price}₽"
class Order:
    def __init__(self):
        self.cart = []  # List to hold dishes in the cart
        self.total_price = 0  # Total price of the order

    def add_dish(self, dish):
        """Adds a dish to the cart and updates the total price"""
        self.cart.append(dish)
        self.total_price += dish.price

    def remove_dish(self, dish_name):
        """Removes a dish by name from the cart and updates the total price"""
        for dish in self.cart:
            if dish.name == dish_name:
                self.cart.remove(dish)
                self.total_price -= dish.price
                break

    def view_cart(self):
        """Displays the contents of the cart and the total price"""
        if not self.cart:
            print("Your cart is empty.")
        else:
            print("Your order:")
            for dish in self.cart:
                print(dish)
            print(f"Total price: {self.total_price}₽")
class Menu:
    def __init__(self):
        """Initializes the menu with some dishes"""
        self.dishes = [
            Dish("Borscht", 150),
            Dish("Dumplings", 200),
            Dish("Salad", 100),
            Dish("Tea", 50)
        ]

    def show_menu(self):
        """Displays the menu"""
        print("Menu:")
        for dish in self.dishes:
            print(dish)
def main():
    menu = Menu()  # Create a menu object
    order = Order()  # Create an order object

    while True:
        # Print the main menu
        print("\nMain Menu:")
        print("1. View menu")
        print("2. Add dish to cart")
        print("3. Remove dish from cart")
        print("4. View cart")
        print("5. Checkout")
        print("6. Exit")

        # Get user's choice
        choice = input("Choose an option: ")

        if choice == '1':
            menu.show_menu()  # Show the menu
        elif choice == '2':
            dish_name = input("Enter the name of the dish to add: ")
            for dish in menu.dishes:
                if dish.name.lower() == dish_name.lower():
                    order.add_dish(dish)  # Add the dish to the cart
                    print(f"{dish.name} added to the cart.")
                    break
            else:
                print("Dish not found in the menu.")
        elif choice == '3':
            dish_name = input("Enter the name of the dish to remove: ")
            order.remove_dish(dish_name)  # Remove the dish from the cart
        elif choice == '4':
            order.view_cart()  # View the cart
        elif choice == '5':
            order.view_cart()
            order.choose_payment()  # Checkout and choose payment method
            break
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
class Order:
    # All previous code...

    def choose_payment(self):
        """Choose payment method"""
        print(f"Total price of the order: {self.total_price}₽")
        payment_method = input("Choose payment method (card / cash): ").lower()
        if payment_method in ['card', 'cash']:
            print(f"You selected {payment_method} payment.")
        else:
            print("Invalid choice.")
