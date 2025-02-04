class Customer:
    def __init__(self, customer_id, first_name, last_name, address, zip_code, password):
        self.id = customer_id  # ID is assigned externally by the calling function
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.zip_code = zip_code
        self.password = password
        self.orders = []  # List of orders placed by the customer
        self.wallet_balance = 100  # Starting wallet balance for each customer

    def deduct_balance(self, amount):
        """Deduct the amount from the customer's wallet."""
        if self.wallet_balance >= amount:
            self.wallet_balance -= amount
            return True
        return False

    def add_balance(self, amount):
        """Add amount to the customer's wallet."""
        self.wallet_balance += amount

class Restaurant:
    def __init__(self, name, address, description, password):
        self.name = name
        self.address = address
        self.description = description
        self.password = password
        self.menu = []  # A list to store menu items
        self.orders = []  # A list to store orders
        self.opening_hours = {}  # {day: (open_time, close_time)}
        self.delivery_radius = []  # List of zip codes
        self.id = None
        self.wallet_balance = 0  # Restaurant's initial balance

    def add_balance(self, amount):
        """ Add amount to restaurant's balance """
        self.wallet_balance += amount


class MenuItem:
    def __init__(self, name, description, price, image=None):
        self.name = name
        self.description = description
        self.price = price
        self.image = image
        self.id = None


import sqlite3
from datetime import datetime

class Order:
    def __init__(self, customer_id, restaurant_id, items, status='in Bearbeitung'):
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.items = items  # List of items with quantity
        self.status = status  # 'in Bearbeitung', 'in Zubereitung', 'storniert', 'abgeschlossen'
        self.timestamp = datetime.now()

    def total_price(self):
        """Calculate the total price for the order"""
        return sum(item['price'] * item['quantity'] for item in self.items)

    def place_order(self):
        """Insert the order into the database and create a notification"""
        conn = sqlite3.connect('lieferspatz.db')
        cursor = conn.cursor()

        # Insert order into orders table
        cursor.execute("INSERT INTO orders (customer_id, restaurant_id, status) VALUES (?, ?, ?)",
                       (self.customer_id, self.restaurant_id, self.status))
        
        # Get the last inserted order ID
        order_id = cursor.lastrowid

        # Insert order items
        for item in self.items:
            cursor.execute("INSERT INTO order_items (order_id, item_name, item_price, quantity) VALUES (?, ?, ?, ?)",
                           (order_id, item['name'], item['price'], item['quantity']))

        # Insert notification for restaurant
        message = f"New order received! Order ID: {order_id}"
        cursor.execute("INSERT INTO notifications (restaurant_id, message) VALUES (?, ?)",
                       (self.restaurant_id, message))

        conn.commit()
        conn.close()
        print(f"Order placed successfully! Order ID: {order_id}, Notification sent.")


 

