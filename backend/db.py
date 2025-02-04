import sqlite3

# Initialize the database (create tables)
def init_db():
    print("Initializing database...")
    conn = sqlite3.connect('lieferspatz.db')
    cursor = conn.cursor()

    # Create customers table
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
    print("Created customers table.")

    # Create restaurants table
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
    print("Created restaurants table.")

    # Create menu_items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        photo_url TEXT,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
    );
    ''')
    print("Created menu_items table.")

    # Create order_items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        item_price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id)
    );
    ''')
    print("Created order_items table.")

    # Create lieferspatz_balance table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lieferspatz_balance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    print("Created lieferspatz_balance table.")


#Cart should be stored in the Database as a table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (item_id) REFERENCES menu_items(id)
    );
    ''')

#Orders for accepting and declining:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    status TEXT DEFAULT 'In Bearbeitung',
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers (id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
    );
    ''')
    
    # Create notifications table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        read_status INTEGER DEFAULT 0,  -- 0 = Unread, 1 = Read
        FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
    );
    ''')
    print("Created notifications table.")

    conn.commit()
    print("Database commit successful.")
    conn.close()
    print("Database connection closed.")

# Insert sample data into the database
def insert_data():
    print("Inserting sample data...")
    conn = sqlite3.connect('lieferspatz.db')
    cursor = conn.cursor()

    # Insert sample customer
    cursor.execute('''
    INSERT INTO customers (first_name, last_name, street_name, house_number, city, zip_code, password)
    VALUES ('John', 'Doe', 'Hauptstr.', '123A', 'Berlin', '10115', 'password123');
    ''')

    # Insert sample restaurant
    cursor.execute('''
    INSERT INTO restaurants (name, street_name, house_number, city, zip_code, description, password)
    VALUES ('Restaurant A', 'Berliner Str.', '456', 'Hamburg', '20095', 'Delicious food!', 'restaurantpassword');
    ''')

    # Insert sample menu item with photo
    cursor.execute('''
    INSERT INTO menu_items (restaurant_id, name, description, price, photo_url)
    VALUES (1, 'Burger', 'A tasty burger', 5.99, 'https://example.com/burger.jpg');
    ''')

    conn.commit()
    print("Sample data inserted successfully.")
    conn.close()
    print("Database connection closed.")

if __name__ == "__main__":
    init_db()  # Ensure the database is initialized when running db.py
