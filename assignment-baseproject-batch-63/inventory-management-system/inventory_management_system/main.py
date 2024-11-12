import json
import os

class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        if not isinstance(product_id, int):
            raise ValueError("Product ID must be an integer.")
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

    def update_product(self, name=None, category=None, price=None, stock_quantity=None):
        if name:
            self.name = name
        if category:
            self.category = category
        if price is not None:
            self.price = price
        if stock_quantity is not None:
            self.stock_quantity = stock_quantity

    def adjust_stock(self, amount):
        self.stock_quantity += amount
        if self.stock_quantity < 0:
            self.stock_quantity = 0  

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'stock_quantity': self.stock_quantity
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id=data['product_id'],
            name=data['name'],
            category=data['category'],
            price=data['price'],
            stock_quantity=data['stock_quantity']
        )


class Inventory:
    def __init__(self, file_path='inventory.json'):
        self.file_path = file_path
        self.products = {}
        self.load_products()

    def load_products(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                for product_data in data:
                    product = Product.from_dict(product_data)
                    self.products[product.product_id] = product
        else:
            self.products = {}

    def save_products(self):
        with open(self.file_path, 'w') as file:
            json.dump([product.to_dict() for product in self.products.values()], file)

    def add_product(self, product):
        if product.product_id in self.products:
            raise ValueError("Product ID already exists.")
        self.products[product.product_id] = product
        self.save_products()

    def update_product(self, product_id, **kwargs):
        if product_id not in self.products:
            raise KeyError("Product not found.")
        self.products[product_id].update_product(**kwargs)
        self.save_products()

    def delete_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            self.save_products()
        else:
            raise KeyError("Product not found.")

    def view_products(self):
        if not self.products:
            print("No products available.")
        for product in self.products.values():
            print(f"ID: {product.product_id}, Name: {product.name}, Category: {product.category}, "
                  f"Price: Rs.{product.price}, Stock: {product.stock_quantity}")

    def search_product(self, keyword):
        found = [p for p in self.products.values() if keyword.lower() in p.name.lower() or keyword.lower() in p.category.lower()]
        if not found:
            print("No products found.")
        else:
            for product in found:
                print(f"ID: {product.product_id}, Name: {product.name}, Category: {product.category}, "
                      f"Price: Rs.{product.price}, Stock: {product.stock_quantity}")

    def filter_products_by_stock(self, threshold=50):
        low_stock = [p for p in self.products.values() if p.stock_quantity < threshold]
        if not low_stock:
            print("All products have sufficient stock.")
        else:
            print("Products with stock below the threshold:")
            for product in low_stock:
                print(f"ID: {product.product_id}, Name: {product.name}, Stock: {product.stock_quantity}")

    def check_stock_levels(self, threshold=50):
        low_stock = [p for p in self.products.values() if p.stock_quantity < threshold]
        if not low_stock:
            print("All products have sufficient stock.")
        else:
            print("Products with low stock:")
            for product in low_stock:
                print(f"ID: {product.product_id}, Name: {product.name}, Stock: {product.stock_quantity}")
                print(f"Restock alert: Consider restocking {product.name}.")

    def adjust_stock(self, product_id, amount):
        if product_id not in self.products:
            raise KeyError("Product not found.")
        self.products[product_id].adjust_stock(amount)
        self.save_products()
        print(f"Stock for product ID {product_id} adjusted by {amount}. New stock: {self.products[product_id].stock_quantity}")


users = {
    "admin": {"password": "admin", "role": "Admin"},
    "user1": {"password": "user123", "role": "User"},
    "user2": {"password": "user456", "role": "User"},
    "usman": {"password": "usman123", "role": "User"},
}

def authenticate(username, password):
    if username in users and users[username]["password"] == password:
        return users[username]["role"]
    else:
        raise ValueError("Invalid username or password.")

def main():
    inventory = Inventory()
    logged_in = False
    role = None

    while True:  
        while not logged_in:
            username = input("Enter username: ")
            password = input("Enter password: ")
            try:
                role = authenticate(username, password)
                logged_in = True
                print(f"Login successful. Hi, {username}!")
                print("Welcome to Inventory Management System")
            except ValueError as e:
                print(e)

        while logged_in:  
            if role == "Admin":
                print("\nOptions: [1] Add Product [2] Update Product [3] Delete Product [4] View Products "
                      "[5] Check Stock [6] Search Product [7] Adjust Stock [8] Logout [9] Exit")
                choice = input("Select an option: ")

                if choice == "1":
                    try:
                        product_id = int(input("Enter product ID: ")) 
                        if product_id in inventory.products:
                            raise ValueError("Product ID already exists.")

                        name = input("Enter product name: ").strip()
                        if not name:
                            raise ValueError("Product name cannot be empty.")
                        
                        category = input("Enter category: ").strip()
                        if not category:
                            raise ValueError("Category cannot be empty.")
                        
                        price_input = input("Enter price: ").strip()
                        if not price_input:
                            raise ValueError("Price cannot be empty.")
                        price = float(price_input)
                        
                        stock_quantity_input = input("Enter stock quantity: ").strip()
                        if not stock_quantity_input:
                            raise ValueError("Stock quantity cannot be empty.")
                        stock_quantity = int(stock_quantity_input)

                        new_product = Product(product_id, name, category, price, stock_quantity)
                        inventory.add_product(new_product)
                        print("Product added successfully.")

                    except ValueError as e:
                        print(f"Error: {e}")


                elif choice == "2":
                    try:
                        product_id = int(input("Enter product ID to update: "))
                        if product_id not in inventory.products:
                            print("Error: Product not found.")
                        else:
                            product = inventory.products[product_id]
                            
                            name = input(f"Enter new product name (press enter to keep '{product.name}'): ") or product.name
                            category = input(f"Enter new category (press enter to keep '{product.category}'): ") or product.category
                            price_input = input(f"Enter new price (press enter to keep '{product.price}'): ")
                            price = float(price_input) if price_input else product.price
                            stock_input = input(f"Enter new stock quantity (press enter to keep '{product.stock_quantity}'): ")
                            stock_quantity = int(stock_input) if stock_input else product.stock_quantity

                            inventory.update_product(
                                product_id, 
                                name=name, 
                                category=category, 
                                price=price, 
                                stock_quantity=stock_quantity
                            )
                            print("Product updated successfully.")
                    except ValueError:
                        print("Error: Invalid input. Please enter valid values.")


                elif choice == "3":
                    try:
                        product_id = int(input("Enter product ID to delete: "))
                        if product_id not in inventory.products:
                            print("Error: Product not found.")
                        else:
                            inventory.delete_product(product_id)
                            print("Product deleted successfully.")
                    except ValueError:
                        print("Error: Invalid input. Please enter an integer.")

                elif choice == "4":
                    inventory.view_products()

                elif choice == "5":
                    inventory.check_stock_levels()

                elif choice == "6":
                    keyword = input("Enter product name or category to search: ")
                    inventory.search_product(keyword)

                elif choice == "7":
                    try:
                        product_id = int(input("Enter product ID to update: "))
                        if product_id not in inventory.products:
                            print("Error: Product not found.")
                        else:    
                            amount = int(input("Enter the amount to adjust (use negative numbers to reduce stock): "))
                            inventory.adjust_stock(product_id, amount)
                    except ValueError:
                        print("Error: Invalid input. Please enter an integer.")
                    except KeyError as e:
                        print(e)

                elif choice == "8":
                    print("Logging out...")
                    logged_in = False  

                elif choice == "9":
                    print("Exiting...")
                    return  

                else:
                    print("Invalid option. Please try again.")

            elif role == "User":
                print("\nOptions: [1] View Products [2] Search Product [3] Logout [4] Exit")
                choice = input("Select an option: ")

                if choice == "1":
                    inventory.view_products()

                elif choice == "2":
                    keyword = input("Enter product name or category to search: ")
                    inventory.search_product(keyword)

                elif choice == "3":
                    print("Logging out...")
                    logged_in = False 

                elif choice == "4":
                    print("Exiting...")
                    return  

                else:
                    print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
