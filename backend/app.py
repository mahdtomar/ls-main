from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

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
CORS(app)

@app.route('/')
def home():
    return "Welcome to Lieferspatz Backend API!"

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

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO customers (first_name, last_name, street_name, house_number, city, zip_code, password, wallet_balance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['first_name'], data['last_name'], data['street_name'], data['house_number'], data['city'], data['zip_code'], data['password'], 100))

        conn.commit()
        customer_id = cursor.lastrowid
        conn.close()

        return jsonify({'success': True, 'customer_id': customer_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Create a new restaurant
@app.route('/restaurant', methods=['POST'])
def create_restaurant():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid or missing JSON payload'}), 400

        required_fields = ['name', 'street_name', 'house_number', 'city', 'zip_code', 'description', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO restaurants (name, street_name, house_number, city, zip_code, description, password)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['street_name'], data['house_number'], data['city'], data['zip_code'], data['description'], data['password']))

        conn.commit()
        restaurant_id = cursor.lastrowid
        conn.close()

        return jsonify({'success': True, 'restaurant_id': restaurant_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#Restaurant Login
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
            return jsonify({'success': True, 'restaurant_id': restaurant[0]}), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Customer login
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
            return jsonify({'success': True, 'customer_id': customer[0]}), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

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
def create_order():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid or missing JSON payload'}), 400

        customer_id = data.get('customer_id')
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
def add_to_cart():
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO cart (customer_id, item_id, quantity) VALUES (?, ?, ?)",
                       (data['customer_id'], data['item_id'], data['quantity']))

        conn.commit()
        conn.close()

        return jsonify({'success': True}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/cart/<int:customer_id>', methods=['GET'])
def view_cart(customer_id):
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


#Remove item from cart
@app.route('/cart/<int:customer_id>', methods=['DELETE'])
def remove_from_cart(customer_id):
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




# ✅ Modify menu item price
@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>', methods=['PUT'])
def update_menu_item(restaurant_id, item_id):
    try:
        data = request.get_json()
        if not data or 'price' not in data:
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
def add_menu_item(restaurant_id):
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
def delete_menu_item(restaurant_id, item_id):
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
def get_order_details(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT id, customer_id, restaurant_id, status, timestamp FROM orders WHERE id = ?', (order_id,))
        order = cursor.fetchone()

        if not order:
            return jsonify({'error': 'Order not found'}), 404

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
    
# ✅ Fetch past orders for a customer
@app.route('/orders/history/<int:customer_id>', methods=['GET'])
def get_past_orders(customer_id):
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
                'items': [{'name': i[0], 'price': i[1], 'quantity': i[2]} for i in items]
            })

        conn.close()
        return jsonify(order_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ✅ Fetch wallet balance for a customer
@app.route('/wallet/customer/<int:customer_id>', methods=['GET'])
def get_customer_wallet_balance(customer_id):
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
def get_restaurant_wallet_balance(restaurant_id):
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
def update_order_status(order_id):
    try:
        data = request.get_json()
        new_status = data.get('status')

        if new_status not in ["In Bearbeitung", "In Zubereitung", "Storniert", "Abgeschlossen"]:
            return jsonify({'error': 'Invalid status'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch restaurant_id before updating status
        cursor.execute("SELECT restaurant_id FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()

        if not order:
            return jsonify({'error': 'Order not found'}), 404

        restaurant_id = order[0]

        # Update order status
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        
        # Insert notification for the restaurant
        notification_message = f"Order {order_id} status updated to {new_status}"
        cursor.execute("INSERT INTO notifications (restaurant_id, message) VALUES (?, ?)", (restaurant_id, notification_message))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Order status updated to {new_status}'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Accept an order
@app.route('/order/<int:order_id>/accept', methods=['PUT'])
def accept_order(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE orders SET status = 'In Zubereitung' WHERE id = ?", (order_id,))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Order not found'}), 404

        # Insert notification for customer
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
def decline_order(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE orders SET status = 'Storniert' WHERE id = ?", (order_id,))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Order not found'}), 404

        # Insert notification for customer
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
def update_business_settings(restaurant_id):
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
def get_notifications(restaurant_id):
    """Fetch notifications for a restaurant, with an option to view read notifications."""
    include_read = request.args.get('include_read', 'false').lower() == 'true'
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if include_read:
        cursor.execute("SELECT id, message, timestamp FROM notifications WHERE restaurant_id = ?", (restaurant_id,))
    else:
        cursor.execute("SELECT id, message, timestamp FROM notifications WHERE restaurant_id = ? AND read_status = 0", (restaurant_id,))
    
    notifications = cursor.fetchall()
    conn.close()

    return jsonify([{"id": n[0], "message": n[1], "timestamp": n[2]} for n in notifications])


@app.route('/notifications/read/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM notifications WHERE id = ?", (notification_id,))
    notification = cursor.fetchone()

    if not notification:
        conn.close()
        return jsonify({'error': 'Notification not found'}), 404

    cursor.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Notification deleted."})



if __name__ == '__main__':
    app.run(debug=True)

