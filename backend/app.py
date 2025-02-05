from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

# Database Path
DB_PATH = os.path.abspath("lieferspatz.db")


def get_db_connection():
    """Returns a connection to the SQLite database"""
    try:
        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(f"Database file not found at {DB_PATH}")

        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = ON")  # Ensures foreign key constraints
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})


@app.route("/")
def home():
    return "Welcome to Lieferspatz Backend API!"


def get_db_connection():
    """Returns a connection to the SQLite database"""
    try:
        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(f"Database file not found at {DB_PATH}")
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = ON")  # Ensures foreign key cons   traints
        return conn
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None


# ✅ Create a new customer
@app.route("/customer", methods=["POST"])
def create_customer():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400

        required_fields = [
            "first_name",
            "last_name",
            "street_name",
            "house_number",
            "city",
            "zip_code",
            "password",
        ]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Get database connection
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()

        # Insert customer data (No need to check if customer exists)
        cursor.execute(
            """
            INSERT INTO customers (first_name, last_name, street_name, house_number, city, zip_code, password, wallet_balance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                data["first_name"],
                data["last_name"],
                data["street_name"],
                data["house_number"],
                data["city"],
                data["zip_code"],
                data["password"],
                100,
            ),
        )

        conn.commit()
        customer_id = cursor.lastrowid
        conn.close()

        return jsonify({"success": True, "customer_id": customer_id}), 201

    except Exception as e:
        print(f"❌ Error creating customer: {e}")  # Log the error for debugging
        return jsonify({"error": str(e)}), 500


@app.route("/restaurant", methods=["POST"])
def create_restaurant():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400

        required_fields = [
            "name",
            "street_name",
            "house_number",
            "city",
            "zip_code",
            "description",
            "password",
        ]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Get database connection
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()

        # Insert restaurant data (No need to check if restaurant exists)
        cursor.execute(
            """
            INSERT INTO restaurants (name, street_name, house_number, city, zip_code, description, password, wallet_balance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                data["name"],
                data["street_name"],
                data["house_number"],
                data["city"],
                data["zip_code"],
                data["description"],
                data["password"],
                0,
            ),
        )

        conn.commit()
        restaurant_id = cursor.lastrowid
        conn.close()

        return jsonify({"success": True, "restaurant_id": restaurant_id}), 201

    except Exception as e:
        print(f"❌ Error creating restaurant: {e}")  # Log the error for debugging
        return jsonify({"error": str(e)}), 500


@app.route("/restaurant/login", methods=["POST"])
def login_restaurant():
    try:
        data = request.get_json()
        name = data.get("name")
        password = data.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM restaurants WHERE name = ? AND password = ?",
            (name, password),
        )
        restaurant = cursor.fetchone()

        conn.close()

        if restaurant:
            return jsonify({"success": True, "restaurant_id": restaurant[0]}), 200
        else:
            return jsonify({"success": False, "error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/customer/login", methods=["POST"])
def login_customer():
    try:
        data = request.get_json()
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM customers WHERE first_name = ? AND last_name = ? AND password = ?",
            (first_name, last_name, password),
        )
        customer = cursor.fetchone()

        conn.close()

        if customer:
            return jsonify({"success": True, "customer_id": customer[0]}), 200
        else:
            return jsonify({"success": False, "error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/customer/profile", methods=["GET"])
def get_customer_profile():
    """Retrieve personal details of a customer by ID"""
    print("customer ID")
    print(request.args)
    try:
        customer_id = request.args.get(
            "customer_id"
        )  # Get customer_id from query parameters
        print(customer_id)
        if not customer_id:
            return jsonify({"error": "Missing customer ID"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Fetch customer details
        cursor.execute(
            """
            SELECT first_name, last_name, street_name, house_number, 
                   city, zip_code
            FROM customers 
            WHERE id = ?
        """,
            (customer_id,),
        )

        customer = cursor.fetchone()
        conn.close()

        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        return (
            jsonify(
                {
                    "first_name": customer[0],
                    "last_name": customer[1],
                    "street_name": customer[2],
                    "house_number": customer[3],
                    "city": customer[4],
                    "zip_code": customer[5],
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Fetch all restaurants, optionally filter by ZIP code
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    try:
        zip_code = request.args.get("zip_code")

        conn = get_db_connection()
        cursor = conn.cursor()

        if zip_code:
            # ✅ Filter restaurants by ZIP code if provided
            cursor.execute(
                """
                SELECT id, name, street_name, house_number, city, zip_code, description 
                FROM restaurants WHERE zip_code = ?
            """,
                (zip_code,),
            )
        else:
            # ✅ Fetch all restaurants if no ZIP code is provided
            cursor.execute(
                """
                SELECT id, name, street_name, house_number, city, zip_code, description 
                FROM restaurants
            """
            )

        restaurants = cursor.fetchall()
        conn.close()

        if not restaurants:
            return jsonify({"message": "No restaurants found"}), 200

        return (
            jsonify(
                [
                    {
                        "id": r[0],
                        "name": r[1],
                        "street_name": r[2],
                        "house_number": r[3],
                        "city": r[4],
                        "zip_code": r[5],
                        "description": r[6],
                    }
                    for r in restaurants
                ]
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Fetch restaurant menu
@app.route("/restaurant/<int:restaurant_id>/menu", methods=["GET"])
def get_restaurant_menu(restaurant_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name, description, price, photo_url
            FROM menu_items WHERE restaurant_id = ?
        """,
            (restaurant_id,),
        )
        menu_items = cursor.fetchall()
        conn.close()

        if not menu_items:
            return jsonify({"message": "No menu items found for this restaurant"}), 200

        return (
            jsonify(
                [
                    {
                        "id": item[0],
                        "name": item[1],
                        "description": item[2],
                        "price": item[3],
                        "photo_url": item[4],
                    }
                    for item in menu_items
                ]
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Create an order without authentication
@app.route("/order", methods=["POST"])
def create_order():
    """Allow any customer to place an order without authentication"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400

        customer_id = data.get("customer_id")
        restaurant_id = data.get("restaurant_id")
        items = data.get("items")

        if not customer_id or not restaurant_id or not items:
            return (
                jsonify(
                    {
                        "error": "Missing required fields: customer_id, restaurant_id, and items"
                    }
                ),
                400,
            )

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Validate customer existence and balance
        cursor.execute(
            "SELECT wallet_balance FROM customers WHERE id = ?", (customer_id,)
        )
        customer = cursor.fetchone()
        if not customer:
            conn.close()
            return jsonify({"error": "Customer not found"}), 404

        total_price = sum(item["price"] * item["quantity"] for item in items)

        if customer[0] < total_price:
            conn.close()
            return jsonify({"error": "Insufficient balance to complete the order"}), 400

        try:
            # ✅ Insert order into `orders` table
            cursor.execute(
                """
                INSERT INTO orders (customer_id, restaurant_id, status, timestamp)
                VALUES (?, ?, 'In Bearbeitung', datetime('now'))
            """,
                (customer_id, restaurant_id),
            )

            order_id = cursor.lastrowid

            # ✅ Insert each item into `order_items`
            for item in items:
                cursor.execute(
                    """
                    INSERT INTO order_items (order_id, item_name, item_price, quantity)
                    VALUES (?, ?, ?, ?)
                """,
                    (order_id, item["name"], item["price"], item["quantity"]),
                )

            # ✅ Deduct payment from customer's wallet
            cursor.execute(
                "UPDATE customers SET wallet_balance = wallet_balance - ? WHERE id = ?",
                (total_price, customer_id),
            )

            # ✅ Payment Distribution (85% to restaurant, 15% to Lieferspatz)
            lieferspatz_fee = total_price * 0.15
            restaurant_earnings = total_price * 0.85

            # ✅ Update restaurant balance
            cursor.execute(
                "UPDATE restaurants SET wallet_balance = wallet_balance + ? WHERE id = ?",
                (restaurant_earnings, restaurant_id),
            )

            # ✅ Store Lieferspatz’s earnings
            cursor.execute(
                "INSERT INTO lieferspatz_balance (amount) VALUES (?)",
                (lieferspatz_fee,),
            )

            # ✅ Insert notification for restaurant
            notification_message = f"New order received! Order ID: {order_id}"
            cursor.execute(
                "INSERT INTO notifications (restaurant_id, message) VALUES (?, ?)",
                (restaurant_id, notification_message),
            )

            # ✅ Commit the entire transaction
            conn.commit()
            conn.close()

            return (
                jsonify(
                    {
                        "success": True,
                        "order_id": order_id,
                        "total_price": total_price,
                        "restaurant_earnings": restaurant_earnings,
                        "lieferspatz_fee": lieferspatz_fee,
                    }
                ),
                201,
            )

        except Exception as e:
            conn.rollback()  # Roll back if an error occurs
            conn.close()
            return jsonify({"error": f"Failed to create order: {e}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Allow customers to review and modify their cart before ordering
cart = {}  # Store temporary cart data


@app.route("/cart", methods=["POST"])
def add_to_cart():
    """Allow any customer to add items to their cart"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400

        customer_id = data.get("customer_id")
        item_id = data.get("item_id")
        quantity = data.get("quantity")

        if not customer_id or not item_id or not quantity:
            return (
                jsonify(
                    {
                        "error": "Missing required fields: customer_id, item_id, and quantity"
                    }
                ),
                400,
            )

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Ensure item exists before adding to cart
        cursor.execute("SELECT id FROM menu_items WHERE id = ?", (item_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "Item not found"}), 404

        # ✅ Insert into cart
        cursor.execute(
            "INSERT INTO cart (customer_id, item_id, quantity) VALUES (?, ?, ?)",
            (customer_id, item_id, quantity),
        )

        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Item added to cart"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ View customer cart without authentication
@app.route("/cart", methods=["GET"])
def view_cart():
    """Allow any customer to view their cart"""
    try:
        customer_id = request.args.get("customer_id")
        if not customer_id:
            return jsonify({"error": "Missing customer ID"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT menu_items.id, menu_items.name, menu_items.price, cart.quantity
            FROM cart
            JOIN menu_items ON cart.item_id = menu_items.id
            WHERE cart.customer_id = ?
        """,
            (customer_id,),
        )

        cart_items = cursor.fetchall()
        conn.close()

        return (
            jsonify(
                [
                    {
                        "item_id": item[0],
                        "name": item[1],
                        "price": item[2],
                        "quantity": item[3],
                    }
                    for item in cart_items
                ]
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Remove item from cart without authentication
@app.route("/cart", methods=["DELETE"])
def remove_from_cart():
    """Allow any customer to remove items from their cart"""
    try:
        customer_id = request.args.get("customer_id")
        item_id = request.args.get("item_id")

        if not customer_id or not item_id:
            return jsonify({"error": "Missing customer_id or item_id"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Ensure the item exists in the customer's cart before attempting deletion
        cursor.execute(
            "SELECT id FROM cart WHERE customer_id = ? AND item_id = ?",
            (customer_id, item_id),
        )
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "Item not found in cart"}), 404

        cursor.execute(
            "DELETE FROM cart WHERE customer_id = ? AND item_id = ?",
            (customer_id, item_id),
        )
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Item removed from cart"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ View customer orders without authentication
@app.route("/customer/orders", methods=["GET"])
def customer_orders():
    """Retrieve all orders for a given customer"""
    try:
        customer_id = request.args.get("customer_id")
        if not customer_id:
            return jsonify({"error": "Missing customer ID"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Fetch all orders for the specified customer
        cursor.execute(
            """
            SELECT orders.id, orders.restaurant_id, orders.status, orders.timestamp, restaurants.name 
            FROM orders
            JOIN restaurants ON orders.restaurant_id = restaurants.id
            WHERE orders.customer_id = ?
        """,
            (customer_id,),
        )
        orders = cursor.fetchall()

        # ✅ Fetch ordered items for each order
        order_list = []
        for order in orders:
            order_id, restaurant_id, status, timestamp, restaurant_name = order

            cursor.execute(
                """
                SELECT item_name, quantity, item_price
                FROM order_items
                WHERE order_id = ?
            """,
                (order_id,),
            )
            items = cursor.fetchall()

            order_list.append(
                {
                    "order_id": order_id,
                    "restaurant_name": restaurant_name,
                    "status": status,
                    "timestamp": timestamp,
                    "items": [
                        {"name": item[0], "quantity": item[1], "price": item[2]}
                        for item in items
                    ],
                }
            )

        conn.close()
        return jsonify({"orders": order_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ View restaurant orders without authentication
@app.route("/restaurant/orders", methods=["GET"])
def restaurant_orders():
    """Retrieve all orders for a given restaurant"""
    try:
        restaurant_id = request.args.get("restaurant_id")
        if not restaurant_id:
            return jsonify({"error": "Missing restaurant ID"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Fetch all orders for the specified restaurant
        cursor.execute(
            """
            SELECT orders.id, orders.customer_id, orders.status, orders.timestamp, 
                   customers.first_name, customers.last_name
            FROM orders
            JOIN customers ON orders.customer_id = customers.id
            WHERE orders.restaurant_id = ?
        """,
            (restaurant_id,),
        )
        orders = cursor.fetchall()

        # ✅ Fetch ordered items for each order
        order_list = []
        for order in orders:
            order_id, customer_id, status, timestamp, first_name, last_name = order

            cursor.execute(
                """
                SELECT item_name, quantity, item_price
                FROM order_items
                WHERE order_id = ?
            """,
                (order_id,),
            )
            items = cursor.fetchall()

            order_list.append(
                {
                    "order_id": order_id,
                    "customer_name": f"{first_name} {last_name}",
                    "status": status,
                    "timestamp": timestamp,
                    "items": [
                        {"name": item[0], "quantity": item[1], "price": item[2]}
                        for item in items
                    ],
                }
            )

        conn.close()
        return jsonify({"orders": order_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Modify menu item price without authentication
@app.route("/restaurant/menu/<int:item_id>", methods=["PUT"])
def update_menu_item(item_id):
    """Allow any restaurant to update a menu item price by providing restaurant_id"""
    try:
        data = request.get_json()
        restaurant_id = data.get("restaurant_id")

        if not restaurant_id or "price" not in data:
            return jsonify({"error": "Missing restaurant_id or price field"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Update menu item price
        cursor.execute(
            """
            UPDATE menu_items 
            SET price = ? 
            WHERE id = ? AND restaurant_id = ?
        """,
            (data["price"], item_id, restaurant_id),
        )

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Menu item not found or unauthorized"}), 404

        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Menu item price updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Add a new menu item
# ✅ Add a new menu item without authentication
@app.route("/restaurant/menu", methods=["POST"])
def add_menu_item():
    """Allow any restaurant to add menu items by providing restaurant_id"""
    try:
        data = request.get_json()
        restaurant_id = data.get("restaurant_id")

        if not restaurant_id or not all(
            k in data for k in ("name", "description", "price")
        ):
            return jsonify({"error": "Missing restaurant_id or required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Insert new menu item
        cursor.execute(
            """
            INSERT INTO menu_items (restaurant_id, name, description, price)
            VALUES (?, ?, ?, ?)
        """,
            (restaurant_id, data["name"], data["description"], data["price"]),
        )

        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Menu item added"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Delete menu item without authentication
@app.route("/restaurant/menu/<int:item_id>", methods=["DELETE"])
def delete_menu_item(item_id):
    """Allow any restaurant to delete menu items by providing restaurant_id"""
    try:
        data = request.get_json()
        restaurant_id = data.get("restaurant_id")

        if not restaurant_id:
            return jsonify({"error": "Missing restaurant_id"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Delete the menu item
        cursor.execute(
            "DELETE FROM menu_items WHERE id = ? AND restaurant_id = ?",
            (item_id, restaurant_id),
        )

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Menu item not found or unauthorized"}), 404

        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Menu item deleted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Get order details without authentication
@app.route("/order/<int:order_id>", methods=["GET"])
def get_order_details(order_id):
    """Retrieve order details without authentication"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, customer_id, restaurant_id, status, timestamp FROM orders WHERE id = ?",
            (order_id,),
        )
        order = cursor.fetchone()

        if not order:
            conn.close()
            return jsonify({"error": "Order not found"}), 404

        # ✅ Fetch order items
        cursor.execute(
            "SELECT item_name, item_price, quantity FROM order_items WHERE order_id = ?",
            (order_id,),
        )
        items = cursor.fetchall()

        order_details = {
            "order_id": order[0],
            "customer_id": order[1],
            "restaurant_id": order[2],
            "status": order[3],
            "timestamp": order[4],
            "items": [{"name": i[0], "price": i[1], "quantity": i[2]} for i in items],
        }

        conn.close()
        return jsonify(order_details), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Retrieve order status without authentication
@app.route("/order/<int:order_id>/status", methods=["GET"])
def get_order_status(order_id):
    """Retrieve the status of an order without authentication"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch order details
        cursor.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()

        if not order:
            conn.close()
            return jsonify({"error": "Order not found"}), 404

        conn.close()
        return jsonify({"order_id": order_id, "status": order[0]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Fetch past orders without authentication
@app.route("/orders/history", methods=["GET"])
def get_past_orders():
    """Fetch past orders for a given customer"""
    print(request.args["customer_ID"])
    try:
        customer_id = request.args.get("customer_ID")
        if not customer_id:
            return jsonify({"error": "Missing customer ID"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, restaurant_id, status, timestamp 
            FROM orders 
            WHERE customer_id = ? 
            ORDER BY timestamp DESC
        """,
            (customer_id,),
        )

        orders = cursor.fetchall()

        if not orders:
            conn.close()
            return jsonify({"message": "No past orders found"}), 200

        # ✅ Fetch order items for each order
        order_list = []
        for order in orders:
            order_id, restaurant_id, status, timestamp = order

            cursor.execute(
                "SELECT item_name, item_price, quantity FROM order_items WHERE order_id = ?",
                (order_id,),
            )
            items = cursor.fetchall()

            order_list.append(
                {
                    "order_id": order_id,
                    "restaurant_id": restaurant_id,
                    "status": status,
                    "timestamp": timestamp,
                    "items": [
                        {"name": item[0], "price": item[1], "quantity": item[2]}
                        for item in items
                    ],
                }
            )

        conn.close()
        return jsonify({"orders": order_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Retrieve customer wallet balance without authentication
@app.route("/wallet/customer", methods=["GET"])
def get_customer_wallet_balance():
    """Retrieve the wallet balance of a given customer"""
    try:
        customer_id = request.args.get("customer_id")
        if not customer_id:
            return jsonify({"error": "Missing customer ID"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT wallet_balance FROM customers WHERE id = ?", (customer_id,)
        )
        balance = cursor.fetchone()
        conn.close()

        if not balance:
            return jsonify({"error": "Customer not found"}), 404

        return jsonify({"customer_id": customer_id, "wallet_balance": balance[0]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Retrieve restaurant wallet balance without authentication
@app.route("/wallet/restaurant", methods=["GET"])
def get_restaurant_wallet_balance():
    """Retrieve the wallet balance of a given restaurant"""
    try:
        restaurant_id = request.args.get("restaurant_id")
        if not restaurant_id:
            return jsonify({"error": "Missing restaurant ID"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT wallet_balance FROM restaurants WHERE id = ?", (restaurant_id,)
        )
        balance = cursor.fetchone()
        conn.close()

        if not balance:
            return jsonify({"error": "Restaurant not found"}), 404

        return (
            jsonify({"restaurant_id": restaurant_id, "wallet_balance": balance[0]}),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Update order status without authentication
@app.route("/order/<int:order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    """Allow any restaurant to update order status by providing restaurant_id"""
    try:
        data = request.get_json()
        restaurant_id = data.get("restaurant_id")
        new_status = data.get("status")

        if not restaurant_id or new_status not in [
            "In Bearbeitung",
            "In Zubereitung",
            "Storniert",
            "Abgeschlossen",
        ]:
            return jsonify({"error": "Missing restaurant_id or invalid status"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Fetch the restaurant_id before updating the status
        cursor.execute("SELECT restaurant_id FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()

        if not order:
            conn.close()
            return jsonify({"error": "Order not found"}), 404

        assigned_restaurant_id = order[0]

        # ✅ Authorization check: Only the assigned restaurant can update the order status
        if int(restaurant_id) != assigned_restaurant_id:
            conn.close()
            return jsonify({"error": "Unauthorized access"}), 403

        # ✅ Update order status
        cursor.execute(
            "UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id)
        )

        # ✅ Insert notification for the customer
        notification_message = f"Order {order_id} status updated to {new_status}"
        cursor.execute(
            "INSERT INTO notifications (customer_id, message) VALUES ((SELECT customer_id FROM orders WHERE id = ?), ?)",
            (order_id, notification_message),
        )

        conn.commit()
        conn.close()
        return (
            jsonify(
                {"success": True, "message": f"Order status updated to {new_status}"}
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Accept an order without authentication
@app.route("/order/<int:order_id>/accept", methods=["PUT"])
def accept_order(order_id):
    """Allow any restaurant to accept an order by providing restaurant_id"""
    try:
        data = request.get_json()
        restaurant_id = data.get("restaurant_id")

        if not restaurant_id:
            return jsonify({"error": "Missing restaurant_id"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Fetch the restaurant_id before accepting the order
        cursor.execute("SELECT restaurant_id FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()

        if not order:
            conn.close()
            return jsonify({"error": "Order not found"}), 404

        assigned_restaurant_id = order[0]

        # ✅ Authorization check: Only the assigned restaurant can accept the order
        if int(restaurant_id) != assigned_restaurant_id:
            conn.close()
            return jsonify({"error": "Unauthorized access"}), 403

        # ✅ Accept Order
        cursor.execute(
            "UPDATE orders SET status = 'In Zubereitung' WHERE id = ?", (order_id,)
        )

        # ✅ Notification: Order Accepted
        notification_message = f"Order {order_id} is now being prepared."
        cursor.execute(
            "INSERT INTO notifications (customer_id, message) VALUES ((SELECT customer_id FROM orders WHERE id = ?), ?)",
            (order_id, notification_message),
        )

        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Order accepted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Decline an order without authentication
@app.route("/order/<int:order_id>/decline", methods=["PUT"])
def decline_order(order_id):
    """Allow any restaurant to decline an order by providing restaurant_id"""
    try:
        data = request.get_json()
        restaurant_id = data.get("restaurant_id")

        if not restaurant_id:
            return jsonify({"error": "Missing restaurant_id"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Fetch the restaurant_id before declining the order
        cursor.execute("SELECT restaurant_id FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()

        if not order:
            conn.close()
            return jsonify({"error": "Order not found"}), 404

        assigned_restaurant_id = order[0]

        # ✅ Authorization check: Only the assigned restaurant can decline the order
        if int(restaurant_id) != assigned_restaurant_id:
            conn.close()
            return jsonify({"error": "Unauthorized access"}), 403

        # ✅ Decline Order
        cursor.execute(
            "UPDATE orders SET status = 'Storniert' WHERE id = ?", (order_id,)
        )

        # ✅ Notification: Order Declined
        notification_message = f"Order {order_id} has been canceled."
        cursor.execute(
            "INSERT INTO notifications (customer_id, message) VALUES ((SELECT customer_id FROM orders WHERE id = ?), ?)",
            (order_id, notification_message),
        )

        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Order declined"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/restaurant/settings", methods=["PUT"])
def update_business_settings():
    """Allow any restaurant to update business settings"""
    try:
        data = request.get_json()
        restaurant_id = data.get("restaurant_id")

        if not restaurant_id or not all(
            k in data for k in ("business_hours", "delivery_radius")
        ):
            return jsonify({"error": "Missing restaurant_id or required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Update restaurant business settings
        cursor.execute(
            """
            UPDATE restaurants 
            SET business_hours = ?, delivery_radius = ? 
            WHERE id = ?
        """,
            (data["business_hours"], data["delivery_radius"], restaurant_id),
        )

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Restaurant not found"}), 404

        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Business settings updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/notifications/restaurant", methods=["GET"])
def get_notifications():
    """Allow any restaurant to fetch its notifications"""
    try:
        restaurant_id = request.args.get("restaurant_id")
        include_read = request.args.get("include_read", "false").lower() == "true"

        if not restaurant_id:
            return jsonify({"error": "Missing restaurant_id"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Fetch restaurant notifications based on read status
        if include_read:
            cursor.execute(
                "SELECT id, message, timestamp FROM notifications WHERE restaurant_id = ?",
                (restaurant_id,),
            )
        else:
            cursor.execute(
                "SELECT id, message, timestamp FROM notifications WHERE restaurant_id = ? AND read_status = 0",
                (restaurant_id,),
            )

        notifications = cursor.fetchall()
        conn.close()

        return (
            jsonify(
                [
                    {"id": n[0], "message": n[1], "timestamp": n[2]}
                    for n in notifications
                ]
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/notifications/customer", methods=["GET"])
def get_customer_notifications():
    """Allow any customer to fetch their notifications"""
    try:
        customer_id = request.args.get("customer_id")

        if not customer_id:
            return jsonify({"error": "Missing customer_id"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Fetch customer notifications that are unread
        cursor.execute(
            "SELECT id, message, timestamp FROM notifications WHERE customer_id = ? AND read_status = 0",
            (customer_id,),
        )
        notifications = cursor.fetchall()
        conn.close()

        return (
            jsonify(
                [
                    {"id": n[0], "message": n[1], "timestamp": n[2]}
                    for n in notifications
                ]
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Restaurant notification delete route
@app.route("/restaurant/notifications/<int:notification_id>", methods=["DELETE"])
def delete_restaurant_notification(notification_id):
    """Allow any restaurant to delete its own notifications"""
    try:
        data = request.get_json()
        restaurant_id = data.get("restaurant_id")

        if not restaurant_id:
            return jsonify({"error": "Missing restaurant_id"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Fetch the restaurant_id associated with the notification
        cursor.execute(
            "SELECT restaurant_id FROM notifications WHERE id = ?", (notification_id,)
        )
        notification = cursor.fetchone()

        if not notification:
            conn.close()
            return jsonify({"error": "Notification not found"}), 404

        assigned_restaurant_id = notification[0]

        # ✅ Authorization check: Only the assigned restaurant can delete the notification
        if int(restaurant_id) != assigned_restaurant_id:
            conn.close()
            return jsonify({"error": "Unauthorized access"}), 403

        # ✅ Delete the notification
        cursor.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
        conn.commit()
        conn.close()

        return (
            jsonify({"success": True, "message": "Notification deleted successfully"}),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/customer/notifications/<int:notification_id>", methods=["DELETE"])
def delete_customer_notification(notification_id):
    """Allow any customer to delete their own notifications"""
    try:
        data = request.get_json()
        customer_id = data.get("customer_id")

        if not customer_id:
            return jsonify({"error": "Missing customer_id"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Fetch the customer_id associated with the notification
        cursor.execute(
            "SELECT customer_id FROM notifications WHERE id = ?", (notification_id,)
        )
        notification = cursor.fetchone()

        if not notification:
            conn.close()
            return jsonify({"error": "Notification not found"}), 404

        assigned_customer_id = notification[0]

        # ✅ Authorization check: Only the assigned customer can delete the notification
        if int(customer_id) != assigned_customer_id:
            conn.close()
            return jsonify({"error": "Unauthorized access"}), 403

        # ✅ Delete the notification
        cursor.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
        conn.commit()
        conn.close()

        return (
            jsonify({"success": True, "message": "Notification deleted successfully"}),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/wallet", methods=["GET"])
def get_balance():
    """Retrieve the wallet balance of a user"""
    try:
        user_id = request.args.get("user_id")
        user_role = request.args.get("user_role")

        if not user_id or not user_role:
            return jsonify({"error": "Missing user_id or user_role"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Determine the correct table based on user role
        table = "customers" if user_role == "customer" else "restaurants"

        # ✅ Fetch wallet balance
        cursor.execute(f"SELECT wallet_balance FROM {table} WHERE id = ?", (user_id,))
        balance = cursor.fetchone()
        conn.close()

        if not balance:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"user_id": user_id, "balance": balance[0]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/payment", methods=["POST"])
def process_payment():
    """Handle payments from a customer to a restaurant"""
    try:
        data = request.get_json()
        required_fields = ["customer_id", "restaurant_id", "order_id", "amount"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        customer_id = data["customer_id"]
        restaurant_id = data["restaurant_id"]
        order_id = data["order_id"]
        total_amount = data["amount"]

        # Platform fee (15%)
        platform_fee = round(total_amount * 0.15, 2)
        restaurant_amount = round(total_amount * 0.85, 2)

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Check if customer has enough balance
        cursor.execute(
            "SELECT wallet_balance FROM customers WHERE id = ?", (customer_id,)
        )
        customer_balance = cursor.fetchone()

        if not customer_balance or customer_balance[0] < total_amount:
            conn.close()
            return jsonify({"error": "Insufficient balance"}), 400

        # ✅ Deduct from customer
        cursor.execute(
            "UPDATE customers SET wallet_balance = wallet_balance - ? WHERE id = ?",
            (total_amount, customer_id),
        )

        # ✅ Add to restaurant
        cursor.execute(
            "UPDATE restaurants SET wallet_balance = wallet_balance + ? WHERE id = ?",
            (restaurant_amount, restaurant_id),
        )

        # ✅ Add to Lieferspatz platform earnings
        cursor.execute(
            "INSERT INTO lieferspatz_balance (amount) VALUES (?)", (platform_fee,)
        )

        # ✅ Log the transaction
        cursor.execute(
            """
            INSERT INTO transactions (customer_id, restaurant_id, order_id, amount, platform_fee)
            VALUES (?, ?, ?, ?, ?)
        """,
            (customer_id, restaurant_id, order_id, total_amount, platform_fee),
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "Payment processed successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/logout", methods=["POST"])
def logout():
    """Handle user logout"""
    return jsonify({"success": True, "message": "User logged out successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
