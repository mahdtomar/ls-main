from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session  # Added for session management
from datetime import timedelta  # Add this import at the top
import sqlite3
import os
from functools import wraps

# Database Path
DB_PATH = os.path.abspath('lieferspatz.db')

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
CORS(app,
     resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
                       "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                       "allow_headers": ["Content-Type"],
                       "supports_credentials": True}},
     expose_headers=["Content-Range", "X-Content-Range"])

# 🔹 Session Configuration
app.config["SECRET_KEY"] = "your_secure_random_secret_key"  # Keep your existing secret key
app.config["SESSION_TYPE"] = "filesystem"  # ✅ Ensures sessions are stored persistently
app.config["SESSION_PERMANENT"] = True  # ✅ Sessions persist across browser refresh
app.config["SESSION_USE_SIGNER"] = True  # ✅ Adds extra security to session cookies
app.config["SESSION_FILE_DIR"] = "./flask_session"  # ✅ Explicit directory for session files
app.config["SESSION_FILE_THRESHOLD"] = 100  # ✅ Limits session file count to avoid overflow

app.config.update(
    SESSION_COOKIE_SECURE=False,  # ✅ Set to False for local dev (Change to True in production)
    SESSION_COOKIE_HTTPONLY=True,  # ✅ Prevents client-side JS from accessing cookies
    SESSION_COOKIE_SAMESITE='Lax',  # ✅ Prevents CSRF while allowing same-site requests
    PERMANENT_SESSION_LIFETIME=timedelta(days=7)  # ✅ Sessions last 7 days
)

Session(app)  # ✅ Initializes Flask-Session


@app.route('/')
def home():
    return "Welcome to Lieferspatz Backend API!"

@app.route('/session')
def check_session():
    return jsonify({"user_id": session.get("user_id"), "role": session.get("role")})


#✅ Add a Session Check Function (Reusable)
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is logged in
            user_id = session.get('user_id')
            if not user_id:
                return jsonify({'error': 'Unauthorized. Please log in.'}), 401
            
            # If role is specified, check if user has correct role
            if role:
                user_role = session.get('role')
                if user_role != role:
                    return jsonify({'error': f'Access denied. Required role: {role}'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

#Logout Route Code
@app.route('/logout', methods=['POST'])
def logout():
    """Logs out the user by clearing the session."""
    session.clear()  # Removes user_id and role from session
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200


# ✅ Create a new customer
@app.route('/customer', methods=['POST'])
def create_customer():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid or missing JSON payload'}), 400

        required_fields = ['first_name', 'last_name', 'street_name', 'house_number', 'city', 'zip_code', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Get database connection
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor()

        # Insert customer data
        cursor.execute('''
            INSERT INTO customers (first_name, last_name, street_name, house_number, city, zip_code, password, wallet_balance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['first_name'], data['last_name'], data['street_name'], data['house_number'], data['city'], data['zip_code'], data['password'], 100))

        conn.commit()
        customer_id = cursor.lastrowid
        conn.close()  # Ensure the connection is closed properly

        return jsonify({'success': True, 'customer_id': customer_id}), 201

    except Exception as e:
        if conn:
            conn.close()  # Ensure connection is closed in case of an error
        print(f"❌ Error creating customer: {e}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 500
    
@app.route('/restaurant', methods=['POST'])
def create_restaurant():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid or missing JSON payload'}), 400

        required_fields = ['name', 'street_name', 'house_number', 'city', 'zip_code', 'description', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Get database connection
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor()

        # Insert restaurant data
        cursor.execute('''
            INSERT INTO restaurants (name, street_name, house_number, city, zip_code, description, password, wallet_balance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['street_name'], data['house_number'], data['city'], data['zip_code'], data['description'], data['password'], 0))

        conn.commit()
        restaurant_id = cursor.lastrowid
        conn.close()  # Ensure the connection is closed properly

        return jsonify({'success': True, 'restaurant_id': restaurant_id}), 201

    except Exception as e:
        if conn:
            conn.close()  # Ensure connection is closed in case of an error
        print(f"❌ Error creating restaurant: {e}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 500
    
# ✅ Restaurant login with session
# ✅ Restaurant login with session
@app.route('/restaurant/login', methods=['POST'])
def login_restaurant():
    try:
        data = request.get_json()
        name = data.get('name')
        password = data.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM restaurants WHERE name = ? AND password = ?", 
                       (name, password))
        restaurant = cursor.fetchone()

        conn.close()

        if restaurant:
            # ✅ Ensure session persists across browser refresh
            session.permanent = True  
            session['user_id'] = restaurant[0]
            session['role'] = 'restaurant'

            # 🔹 Force Flask to save session changes
            session.modified = True  

            print("✅ Session set:", dict(session))  # Debugging output

            return jsonify({'success': True, 'restaurant_id': restaurant[0]}), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500




# ✅ Customer login with session
@app.route('/customer/login', methods=['POST'])
def login_customer():
    try:
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM customers WHERE first_name = ? AND last_name = ? AND password = ?", 
                       (first_name, last_name, password))
        customer = cursor.fetchone()

        conn.close()

        if customer:
            # ✅ Ensure session persists across browser refresh
            session.permanent = True  
            session['user_id'] = customer[0]
            session['role'] = 'customer'

            # 🔹 Force Flask to save session changes
            session.modified = True  

            print("✅ Session set:", dict(session))  # Debugging output

            return jsonify({'success': True, 'customer_id': customer[0]}), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/customer/<int:customer_id>/profile', methods=['GET'])
@login_required('customer')  # Only customers can view their own profile
def get_customer_profile(customer_id):
    """Retrieve personal details of the logged-in customer"""
    if session['user_id'] != customer_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT first_name, last_name, street_name, house_number, 
                   city, zip_code
            FROM customers 
            WHERE id = ?
        """, (customer_id,))
        
        customer = cursor.fetchone()
        conn.close()

        if not customer:
            return jsonify({'error': 'Customer not found'}), 404

        return jsonify({
            'first_name': customer[0],
            'last_name': customer[1],
            'street_name': customer[2],
            'house_number': customer[3],
            'city': customer[4],
            'zip_code': customer[5]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Filter restaurants based on delivery ZIP code
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    try:
        zip_code = request.args.get('zip_code')
        if not zip_code:
            return jsonify({'error': 'ZIP code is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, street_name, house_number, city, zip_code, description FROM restaurants WHERE zip_code = ?", (zip_code,))
        restaurants = cursor.fetchall()
        conn.close()

        if not restaurants:
            return jsonify({'message': 'No restaurants deliver to this ZIP code'}), 200

        return jsonify([{
            'id': r[0],
            'name': r[1],
            'street_name': r[2],
            'house_number': r[3],
            'city': r[4],
            'zip_code': r[5],
            'description': r[6]
        } for r in restaurants]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Fetch restaurant menu
@app.route('/restaurant/<int:restaurant_id>/menu', methods=['GET'])
def get_restaurant_menu(restaurant_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, description, price FROM menu_items WHERE restaurant_id = ?", (restaurant_id,))
        menu_items = cursor.fetchall()
        conn.close()

        if not menu_items:
            return jsonify({'message': 'No menu items found for this restaurant'}), 200

        return jsonify([
            {'id': item[0], 'name': item[1], 'description': item[2], 'price': item[3]}
            for item in menu_items
        ]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Create an order
@app.route('/order', methods=['POST'])
@login_required('customer')  # Only customers can place orders
def create_order():
    """Allow only the logged-in customer to place an order"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid or missing JSON payload'}), 400

        customer_id = session['user_id']  # 🔹 Use session to ensure only the logged-in customer is making the order
        restaurant_id = data.get('restaurant_id')
        items = data.get('items')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Validate customer existence and balance
        cursor.execute("SELECT wallet_balance FROM customers WHERE id = ?", (customer_id,))
        customer = cursor.fetchone()
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404

        total_price = sum(item['price'] * item['quantity'] for item in items)

        if customer[0] < total_price:
            return jsonify({'error': 'Insufficient balance to complete the order'}), 400

        try:
            # Insert order into `orders` table
            cursor.execute('''
                INSERT INTO orders (customer_id, restaurant_id, status, timestamp)
                VALUES (?, ?, 'In Bearbeitung', datetime('now'))
            ''', (customer_id, restaurant_id))

            order_id = cursor.lastrowid

            # Insert each item into `order_items`
            for item in items:
                cursor.execute('''
                    INSERT INTO order_items (order_id, item_name, item_price, quantity)
                    VALUES (?, ?, ?, ?)
                ''', (order_id, item['name'], item['price'], item['quantity']))

            # Deduct payment from customer's wallet
            cursor.execute("UPDATE customers SET wallet_balance = wallet_balance - ? WHERE id = ?", (total_price, customer_id))

            # Payment Distribution (85% to restaurant, 15% to Lieferspatz)
            lieferspatz_fee = total_price * 0.15
            restaurant_earnings = total_price * 0.85

            # Update restaurant balance
            cursor.execute("UPDATE restaurants SET wallet_balance = wallet_balance + ? WHERE id = ?", (restaurant_earnings, restaurant_id))

            # Store Lieferspatz’s earnings
            cursor.execute("INSERT INTO lieferspatz_balance (amount) VALUES (?)", (lieferspatz_fee,))

            # Insert notification for restaurant
            notification_message = f"New order received! Order ID: {order_id}"
            cursor.execute("INSERT INTO notifications (restaurant_id, message) VALUES (?, ?)", (restaurant_id, notification_message))

            # Commit the entire transaction
            conn.commit()
            conn.close()

            return jsonify({
                'success': True,
                'order_id': order_id,
                'total_price': total_price,
                'restaurant_earnings': restaurant_earnings,
                'lieferspatz_fee': lieferspatz_fee
            }), 201

        except Exception as e:
            conn.rollback()  # Roll back if an error occurs
            conn.close()
            return jsonify({'error': f'Failed to create order: {e}'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500




#Allow customers to review and modify thier cart before ordering
cart = {}  # Store temporary cart data

@app.route('/cart', methods=['POST'])
@login_required('customer')  # Only customers can add to cart
def add_to_cart():
    """Allow only the logged-in customer to add items to their cart"""
    try:
        data = request.get_json()
        customer_id = session['user_id']  # 🔹 Use session to ensure ownership

        if data['customer_id'] != customer_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO cart (customer_id, item_id, quantity) VALUES (?, ?, ?)",
                       (customer_id, data['item_id'], data['quantity']))

        conn.commit()
        conn.close()

        return jsonify({'success': True}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/cart/<int:customer_id>', methods=['GET'])
@login_required('customer')  # Only customers can view their cart
def view_cart(customer_id):
    """Allow only the logged-in customer to view their cart"""
    if session['user_id'] != customer_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT menu_items.id, menu_items.name, menu_items.price, cart.quantity
            FROM cart
            JOIN menu_items ON cart.item_id = menu_items.id
            WHERE cart.customer_id = ?
        ''', (customer_id,))

        cart_items = cursor.fetchall()
        conn.close()

        return jsonify([{'item_id': item[0], 'name': item[1], 'price': item[2], 'quantity': item[3]} for item in cart_items])

    except Exception as e:
        return jsonify({'error': str(e)}), 500



#Remove item from cart
@app.route('/cart/<int:customer_id>', methods=['DELETE'])
@login_required('customer')  # Only customers can remove items from their cart
def remove_from_cart(customer_id):
    """Allow only the logged-in customer to remove items from their cart"""
    if session['user_id'] != customer_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        item_id = request.args.get('item_id')
        if not item_id:
            return jsonify({'error': 'Item ID is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM cart WHERE customer_id = ? AND item_id = ?", (customer_id, item_id))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Item removed from cart'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# View Customer Orders (Now Includes Ordered Items)
@app.route('/customer/orders', methods=['GET'])
@login_required('customer')
def customer_orders():
    customer_id = session['user_id']  # Get customer ID from session

    conn = get_db_connection()
    cursor = conn.cursor()

    # 🔹 Fetch all orders for the logged-in customer
    cursor.execute("""
        SELECT orders.id, orders.restaurant_id, orders.status, orders.timestamp, restaurants.name 
        FROM orders
        JOIN restaurants ON orders.restaurant_id = restaurants.id
        WHERE orders.customer_id = ?
    """, (customer_id,))
    orders = cursor.fetchall()

    # 🔹 Fetch ordered items for each order
    order_list = []
    for order in orders:
        order_id, restaurant_id, status, timestamp, restaurant_name = order
        
        cursor.execute("""
            SELECT item_name, quantity, item_price
            FROM order_items
            WHERE order_id = ?
        """, (order_id,))
        items = cursor.fetchall()

        order_list.append({
            "order_id": order_id,
            "restaurant_name": restaurant_name,
            "status": status,
            "timestamp": timestamp,
            "items": [{"name": item[0], "quantity": item[1], "price": item[2]} for item in items]
        })

    conn.close()
    return jsonify({'orders': order_list}), 200



# View Restaurant Orders (Now Includes Ordered Items & Customer Info)
@app.route('/restaurant/orders', methods=['GET'])
@login_required('restaurant')
def restaurant_orders():
    restaurant_id = session['user_id']  # Get restaurant ID from session

    conn = get_db_connection()
    cursor = conn.cursor()

    # 🔹 Fetch all orders for this restaurant
    cursor.execute("""
        SELECT orders.id, orders.customer_id, orders.status, orders.timestamp, 
               customers.first_name, customers.last_name
        FROM orders
        JOIN customers ON orders.customer_id = customers.id
        WHERE orders.restaurant_id = ?
    """, (restaurant_id,))
    orders = cursor.fetchall()

    # 🔹 Fetch ordered items for each order
    order_list = []
    for order in orders:
        order_id, customer_id, status, timestamp, first_name, last_name = order
        
        cursor.execute("""
            SELECT item_name, quantity, item_price
            FROM order_items
            WHERE order_id = ?
        """, (order_id,))
        items = cursor.fetchall()

        order_list.append({
            "order_id": order_id,
            "customer_name": f"{first_name} {last_name}",
            "status": status,
            "timestamp": timestamp,
            "items": [{"name": item[0], "quantity": item[1], "price": item[2]} for item in items]
        })

    conn.close()
    return jsonify({'orders': order_list}), 200






# ✅ Modify menu item price
@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>', methods=['PUT'])
@login_required('restaurant')
def update_menu_item(restaurant_id, item_id):
    if session['user_id'] != restaurant_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        data = request.get_json()
        if 'price' not in data:
            return jsonify({'error': 'Missing price field'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE menu_items 
            SET price = ? 
            WHERE id = ? AND restaurant_id = ?
        ''', (data['price'], item_id, restaurant_id))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Menu item not found'}), 404

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Menu item price updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
#Add Menu Management (Add/Edit/Delete items)
# ✅ Add a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu', methods=['POST'])
@login_required('restaurant')
def add_menu_item(restaurant_id):
    if session['user_id'] != restaurant_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        data = request.get_json()
        if not all(k in data for k in ('name', 'description', 'price')):
            return jsonify({'error': 'Missing required fields'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO menu_items (restaurant_id, name, description, price)
            VALUES (?, ?, ?, ?)
        ''', (restaurant_id, data['name'], data['description'], data['price']))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Menu item added'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# ✅ Delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>', methods=['DELETE'])
@login_required('restaurant')
def delete_menu_item(restaurant_id, item_id):
    if session['user_id'] != restaurant_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM menu_items WHERE id = ? AND restaurant_id = ?", (item_id, restaurant_id))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Menu item not found'}), 404

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Menu item deleted'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# ✅ Get order details
@app.route('/order/<int:order_id>', methods=['GET'])
@login_required()  # Requires login but allows both customers & restaurants
def get_order_details(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT id, customer_id, restaurant_id, status, timestamp FROM orders WHERE id = ?', (order_id,))
        order = cursor.fetchone()

        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # 🔹 Authorization check: Allow only the order's customer or restaurant
        user_id = session['user_id']
        user_role = session['role']

        if user_role == 'customer' and user_id != order[1]:  # Check customer ownership
            return jsonify({'error': 'Unauthorized access'}), 403
        if user_role == 'restaurant' and user_id != order[2]:  # Check restaurant ownership
            return jsonify({'error': 'Unauthorized access'}), 403

        # Fetch order items
        cursor.execute('SELECT item_name, item_price, quantity FROM order_items WHERE order_id = ?', (order_id,))
        items = cursor.fetchall()

        order_details = {
            'order_id': order[0],
            'customer_id': order[1],
            'restaurant_id': order[2],
            'status': order[3],
            'timestamp': order[4],
            'items': [{'name': i[0], 'price': i[1], 'quantity': i[2]} for i in items]
        }

        conn.close()
        return jsonify(order_details), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



    # ✅ Retrieve order status
@app.route('/order/<int:order_id>/status', methods=['GET'])
@login_required()  # Requires login but allows both customers & restaurants
def get_order_status(order_id):
    """Retrieve the status of an order"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch order details
        cursor.execute("SELECT customer_id, restaurant_id, status FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()

        if not order:
            conn.close()
            return jsonify({"error": "Order not found"}), 404

        customer_id, restaurant_id, status = order

        # 🔹 Authorization check: Only the customer or the restaurant can access the order status
        user_id = session['user_id']
        user_role = session['role']

        if user_role == 'customer' and user_id != customer_id:  # Check customer ownership
            conn.close()
            return jsonify({"error": "Unauthorized access"}), 403
        if user_role == 'restaurant' and user_id != restaurant_id:  # Check restaurant ownership
            conn.close()
            return jsonify({"error": "Unauthorized access"}), 403

        conn.close()
        return jsonify({"order_id": order_id, "status": status}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
@app.route('/orders/history/<int:customer_id>', methods=['GET'])
@login_required('customer')  # Only customers can access this route
def get_past_orders(customer_id):
    """Fetch past orders for the logged-in customer"""
    if session['user_id'] != customer_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, restaurant_id, status, timestamp 
            FROM orders 
            WHERE customer_id = ? 
            ORDER BY timestamp DESC
        ''', (customer_id,))

        orders = cursor.fetchall()

        if not orders:
            conn.close()
            return jsonify({'message': 'No past orders found'}), 200

        # Fetch order items for each order
        order_list = []
        for order in orders:
            cursor.execute("SELECT item_name, item_price, quantity FROM order_items WHERE order_id = ?", (order[0],))
            items = cursor.fetchall()

            order_list.append({
                'order_id': order[0],
                'restaurant_id': order[1],
                'status': order[2],
                'timestamp': order[3],
                'items': [{
                    'name': item[0],
                    'price': item[1],
                    'quantity': item[2]
                } for item in items]
            })

        conn.close()
        return jsonify({'orders': order_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# ✅ Fetch wallet balance for a customer
@app.route('/wallet/customer/<int:customer_id>', methods=['GET'])
@login_required('customer')  # Only customers can access this route
def get_customer_wallet_balance(customer_id):
    """Retrieve the wallet balance of the logged-in customer"""
    if session['user_id'] != customer_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT wallet_balance FROM customers WHERE id = ?", (customer_id,))
        balance = cursor.fetchone()
        conn.close()

        if not balance:
            return jsonify({'error': 'Customer not found'}), 404

        return jsonify({'customer_id': customer_id, 'wallet_balance': balance[0]}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# ✅ Fetch wallet balance for a restaurant
@app.route('/wallet/restaurant/<int:restaurant_id>', methods=['GET'])
@login_required('restaurant')  # Only restaurants can access this route
def get_restaurant_wallet_balance(restaurant_id):
    """Allow only the logged-in restaurant to view its wallet balance"""
    if session['user_id'] != restaurant_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT wallet_balance FROM restaurants WHERE id = ?", (restaurant_id,))
        balance = cursor.fetchone()
        conn.close()

        if not balance:
            return jsonify({'error': 'Restaurant not found'}), 404

        return jsonify({'restaurant_id': restaurant_id, 'wallet_balance': balance[0]}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


    
@app.route('/order/<int:order_id>/status', methods=['PUT'])
@login_required('restaurant')  # Only restaurants can update order statuses
def update_order_status(order_id):
    """Allow only the assigned restaurant to update order status"""
    try:
        data = request.get_json()
        new_status = data.get('status')

        if new_status not in ["In Bearbeitung", "In Zubereitung", "Storniert", "Abgeschlossen"]:
            return jsonify({'error': 'Invalid status'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the restaurant_id before updating the status
        cursor.execute("SELECT restaurant_id FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()

        if not order:
            conn.close()
            return jsonify({'error': 'Order not found'}), 404

        restaurant_id = order[0]

        # 🔹 Authorization check: Only the assigned restaurant can update the order status
        if session['user_id'] != restaurant_id:
            conn.close()
            return jsonify({'error': 'Unauthorized access'}), 403

        # Update order status
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))

        # Insert notification for the customer
        notification_message = f"Order {order_id} status updated to {new_status}"
        cursor.execute("INSERT INTO notifications (customer_id, message) VALUES ((SELECT customer_id FROM orders WHERE id = ?), ?)",
                       (order_id, notification_message))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Order status updated to {new_status}'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Accept an order
@app.route('/order/<int:order_id>/accept', methods=['PUT'])
@login_required('restaurant')  # Only restaurants can accept orders
def accept_order(order_id):
    """Allow only the assigned restaurant to accept an order"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the restaurant_id before accepting the order
        cursor.execute("SELECT restaurant_id FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()

        if not order:
            conn.close()
            return jsonify({'error': 'Order not found'}), 404

        restaurant_id = order[0]

        # 🔹 Authorization check: Only the assigned restaurant can accept the order
        if session['user_id'] != restaurant_id:
            conn.close()
            return jsonify({'error': 'Unauthorized access'}), 403

        # Accept Order
        cursor.execute("UPDATE orders SET status = 'In Zubereitung' WHERE id = ?", (order_id,))

        # Notification: Order Accepted
        notification_message = f"Order {order_id} is now being prepared."
        cursor.execute("INSERT INTO notifications (customer_id, message) VALUES ((SELECT customer_id FROM orders WHERE id = ?), ?)",
        (order_id, notification_message))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Order accepted'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# ✅ Decline an order
@app.route('/order/<int:order_id>/decline', methods=['PUT'])
@login_required('restaurant')  # Only restaurants can decline orders
def decline_order(order_id):
    """Allow only the assigned restaurant to decline an order"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the restaurant_id before declining the order
        cursor.execute("SELECT restaurant_id FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()

        if not order:
            conn.close()
            return jsonify({'error': 'Order not found'}), 404

        restaurant_id = order[0]

        # 🔹 Authorization check: Only the assigned restaurant can decline the order
        if session['user_id'] != restaurant_id:
            conn.close()
            return jsonify({'error': 'Unauthorized access'}), 403

        # Decline Order
        cursor.execute("UPDATE orders SET status = 'Storniert' WHERE id = ?", (order_id,))

        # Notification: Order Declined
        notification_message = f"Order {order_id} has been canceled."
        cursor.execute("INSERT INTO notifications (customer_id, message) VALUES ((SELECT customer_id FROM orders WHERE id = ?), ?)",
                       (order_id, notification_message))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Order declined'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Update business settings (Operating Hours & Delivery Radius)
@app.route('/restaurant/<int:restaurant_id>/settings', methods=['PUT'])
@login_required('restaurant')  # Only restaurants can access this route
def update_business_settings(restaurant_id):
    """Allow only the restaurant owner to update business settings"""
    if session['user_id'] != restaurant_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        data = request.get_json()
        if not all(k in data for k in ('business_hours', 'delivery_radius')):
            return jsonify({'error': 'Missing required fields'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE restaurants 
            SET business_hours = ?, delivery_radius = ? 
            WHERE id = ?
        ''', (data['business_hours'], data['delivery_radius'], restaurant_id))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Restaurant not found'}), 404

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Business settings updated'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/notifications/<int:restaurant_id>', methods=['GET'])
@login_required('restaurant')  # Only restaurants can access this route
def get_notifications(restaurant_id):
    """Allow only the logged-in restaurant to fetch its notifications"""
    if session['user_id'] != restaurant_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        include_read = request.args.get('include_read', 'false').lower() == 'true'
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if include_read:
            cursor.execute("SELECT id, message, timestamp FROM notifications WHERE restaurant_id = ?", (restaurant_id,))
        else:
            cursor.execute("SELECT id, message, timestamp FROM notifications WHERE restaurant_id = ? AND read_status = 0", (restaurant_id,))
        
        notifications = cursor.fetchall()
        conn.close()

        return jsonify([{"id": n[0], "message": n[1], "timestamp": n[2]} for n in notifications]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/notifications/<int:customer_id>', methods=['GET'])
@login_required('customer')
def get_customer_notifications(customer_id):
    """Allow only the logged-in customer to fetch their notifications"""
    if session['user_id'] != customer_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, message, timestamp FROM notifications WHERE customer_id = ? AND read_status = 0", 
                       (customer_id,))
        notifications = cursor.fetchall()
        conn.close()

        return jsonify([{"id": n[0], "message": n[1], "timestamp": n[2]} for n in notifications]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Restaurant notification delete route
@app.route('/restaurant/notifications/<int:notification_id>', methods=['DELETE'])
@login_required('restaurant')  # Only restaurants can delete their notifications
def delete_restaurant_notification(notification_id):
    """Allow only the logged-in restaurant to delete its own notifications"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the restaurant_id associated with the notification
        cursor.execute("SELECT restaurant_id FROM notifications WHERE id = ?", (notification_id,))
        notification = cursor.fetchone()

        if not notification:
            conn.close()
            return jsonify({'error': 'Notification not found'}), 404

        restaurant_id = notification[0]

        # Authorization check: Only the assigned restaurant can delete the notification
        if session['user_id'] != restaurant_id:
            conn.close()
            return jsonify({'error': 'Unauthorized access'}), 403

        # Delete the notification
        cursor.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Notification deleted successfully"}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Customer notification delete route
@app.route('/customer/notifications/<int:notification_id>', methods=['DELETE'])
@login_required('customer')  # Only customers can delete their notifications
def delete_customer_notification(notification_id):
    """Allow only the logged-in customer to delete their own notifications"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the customer_id associated with the notification
        cursor.execute("SELECT customer_id FROM notifications WHERE id = ?", (notification_id,))
        notification = cursor.fetchone()

        if not notification:
            conn.close()
            return jsonify({'error': 'Notification not found'}), 404

        customer_id = notification[0]

        # Authorization check: Only the assigned customer can delete the notification
        if session['user_id'] != customer_id:
            conn.close()
            return jsonify({'error': 'Unauthorized access'}), 403

        # Delete the notification
        cursor.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Notification deleted successfully"}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



    # ✅ Virtual Wallet System

# Get user balance
@app.route('/wallet/<int:user_id>', methods=['GET'])
@login_required()  # Requires login, allows both customers & restaurants
def get_balance(user_id):
    """Retrieve the wallet balance of the logged-in user"""
    if session['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
        balance = cursor.fetchone()
        conn.close()

        if not balance:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({"user_id": user_id, "balance": balance[0]}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Process Payment (Customer to Restaurant & Platform Fee)
@app.route('/payment', methods=['POST'])
def process_payment():
    """Handle payments from customer to restaurant with Lieferspatz platform fee"""
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

        # Check if customer has enough balance
        cursor.execute("SELECT balance FROM users WHERE id = ?", (customer_id,))
        customer_balance = cursor.fetchone()
        if not customer_balance or customer_balance[0] < total_amount:
            return jsonify({"error": "Insufficient balance"}), 400

        # Deduct from customer
        cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (total_amount, customer_id))

        # Add to restaurant
        cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (restaurant_amount, restaurant_id))

        # Add to Lieferspatz platform (hidden, only in DB)
        cursor.execute("UPDATE users SET balance = balance + ? WHERE id = 0", (platform_fee,))  # ID 0 = Lieferspatz

        # Log the transaction
        cursor.execute("""
            INSERT INTO transactions (customer_id, restaurant_id, order_id, amount, platform_fee)
            VALUES (?, ?, ?, ?, ?)
        """, (customer_id, restaurant_id, order_id, total_amount, platform_fee))

        conn.commit()
        conn.close()

        return jsonify({"message": "Payment processed successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)

