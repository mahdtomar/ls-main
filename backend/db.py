import sqlite3
import os

DB_PATH = os.path.abspath('lieferspatz.db')

# ✅ Function to get a database connection
def get_db_connection():
    """Returns a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = ON")  # Ensure foreign keys work
        return conn
    except Exception as e:
        raise RuntimeError(f"❌ Database connection error: {e}")

# ✅ Initialize the database (create tables)
def init_db():
    print("Initializing database...")
    conn = get_db_connection()
    if not conn:
        print("❌ Database connection failed.")
        return
    cursor = conn.cursor()

    # Customers Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        street_name TEXT NOT NULL, 
        house_number TEXT NOT NULL,
        city TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        password TEXT NOT NULL,
        wallet_balance REAL DEFAULT 100.0
    );
    ''')
    print("✅ Created customers table.")

    # Restaurants Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        street_name TEXT NOT NULL,
        house_number TEXT NOT NULL,
        city TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        description TEXT,
        password TEXT NOT NULL,
        wallet_balance REAL DEFAULT 0.0
    );
    ''')
    print("✅ Created restaurants table.")

    # Transactions Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        restaurant_id INTEGER NOT NULL,
        order_id INTEGER NOT NULL,
        amount REAL NOT NULL CHECK (amount >= 0),  
        platform_fee REAL NOT NULL CHECK (platform_fee >= 0),  
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    );
    ''')
    print("✅ Created transactions table.")

    # Menu Items Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        photo_url TEXT,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
    );
    ''')
    print("✅ Created menu_items table.")

    # Orders Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        restaurant_id INTEGER NOT NULL,
        status TEXT DEFAULT 'In Bearbeitung',
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
    );
    ''')
    print("✅ Created orders table.")

    # Order Items Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL CHECK (quantity > 0),
        item_price REAL NOT NULL CHECK (item_price >= 0),
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    );
    ''')
    print("✅ Created order_items table.")

    # Cart Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
        FOREIGN KEY (item_id) REFERENCES menu_items(id) ON DELETE CASCADE
    );
    ''')
    print("✅ Created cart table.")

    # Lieferspatz Balance Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lieferspatz_balance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    print("✅ Created lieferspatz_balance table.")

    # Notifications Table (Improved foreign keys)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER DEFAULT NULL,
        restaurant_id INTEGER DEFAULT NULL,
        message TEXT NOT NULL,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        read_status INTEGER DEFAULT 0,
        FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE SET NULL
    );
    ''')
    print("✅ Created notifications table.")

    conn.commit()
    conn.close()
    print("✅ Database initialization complete.")

# ✅ Insert Sample Data (Only if Empty)
def insert_data():
    print("📌 Inserting sample data (if needed)...")
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Insert Sample Customer
        cursor.execute("SELECT COUNT(*) FROM customers")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
            INSERT INTO customers (first_name, last_name, street_name, house_number, city, zip_code, password)
            VALUES ('John', 'Doe', 'Hauptstr.', '123A', 'Berlin', '10115', 'password123');
            ''')
            print("✅ Inserted sample customer.")

        # Insert Sample Restaurant
        cursor.execute("SELECT COUNT(*) FROM restaurants")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
            INSERT INTO restaurants (name, street_name, house_number, city, zip_code, description, password)
            VALUES ('Restaurant A', 'Berliner Str.', '456', 'Hamburg', '20095', 'Delicious food!', 'restaurantpassword');
            ''')
            print("✅ Inserted sample restaurant.")

        # Insert Sample Menu Item
        cursor.execute("SELECT COUNT(*) FROM menu_items")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
            INSERT INTO menu_items (restaurant_id, name, description, price, photo_url)
            VALUES (1, 'Burger', 'A tasty burger', 5.99, 'https://example.com/burger.jpg');
            ''')
            print("✅ Inserted sample menu item.")

        conn.commit()
    print("✅ Sample data insertion complete.")

# ✅ Auto-run when db.py is executed
if __name__ == "__main__":
    init_db()
    insert_data()
