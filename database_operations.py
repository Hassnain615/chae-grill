import sqlite3
import datetime

def create_database():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        price REAL NOT NULL,
        description TEXT,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY,
        customer_name TEXT,
        total_amount REAL NOT NULL,
        date TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bill_items (
        id INTEGER PRIMARY KEY,
        bill_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (bill_id) REFERENCES bills (id),
        FOREIGN KEY (item_id) REFERENCES menu_items (id)
    )
    ''')

    # Check if admin user exists, if not create one
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ('admin', 'admin123', 'admin'))

    # Check if categories exist, if not add default ones
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        categories = [
            "Pizza", "Pasta", "Steaks", "Starters", "Burger",
            "Shawarma / Paratha", "Wraps", "Sandwich", "Coffee & Chai", "Dessert", "Beverage"
        ]
        for category in categories:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (category,))

    # Check if menu items exist, if not add sample items from the menu
    cursor.execute("SELECT COUNT(*) FROM menu_items")
    if cursor.fetchone()[0] == 0:
        # Get category IDs
        cursor.execute("SELECT id, name FROM categories")
        categories = {name: id for id, name in cursor.fetchall()}

        # Add menu items
        menu_items = [
            # Pizza items
            (categories["Pizza"], "Chicken Tikka", 379, "Small size"),
            (categories["Pizza"], "Chicken Tikka", 709, "Regular size"),
            (categories["Pizza"], "Chicken Tikka", 1119, "Large size"),
            (categories["Pizza"], "Chicken Fajita", 379, "Small size"),
            (categories["Pizza"], "Chicken Fajita", 709, "Regular size"),
            (categories["Pizza"], "Chicken Fajita", 1119, "Large size"),

            # Pasta items
            (categories["Pasta"], "Fettucine Alfredo With White Sauce", 605, ""),
            (categories["Pasta"], "Chicken Chowmien", 459, ""),
            (categories["Pasta"], "Penny Pasta With white Sauce", 605, ""),

            # Steaks
            (categories["Steaks"], "B.B.Q Steak with Spicy Sauce", 999, ""),
            (categories["Steaks"], "Terragone Steak", 999, ""),
            (categories["Steaks"], "Mexican Steak", 999, ""),
            (categories["Steaks"], "Mushroom Steak", 999, ""),
            (categories["Steaks"], "Black Pepper Steak", 999, ""),

            # Starters
            (categories["Starters"], "Behari Spin Roll", 515, ""),
            (categories["Starters"], "Behari Spin Roll Platter", 839, ""),
            (categories["Starters"], "French Fries Large", 269, ""),
            (categories["Starters"], "Masala Fries Large", 285, ""),
            (categories["Starters"], "Loaded Fries", 499, ""),

            # Burger
            (categories["Burger"], "Chicken Zinger Burger", 429, ""),
            (categories["Burger"], "Double Decker Zinger Burger", 539, ""),
            (categories["Burger"], "Cheesy Chicken Zinger Burger", 469, ""),
            (categories["Burger"], "Chicken Chapli Burger", 319, ""),
            (categories["Burger"], "Chicken Patty Burger", 319, ""),

            # Shawarma / Paratha
            (categories["Shawarma / Paratha"], "Arabian Shawarma Large", 199, ""),
            (categories["Shawarma / Paratha"], "Feast Roll", 369, ""),
            (categories["Shawarma / Paratha"], "Platter Shawarma", 479, ""),
            (categories["Shawarma / Paratha"], "Kabab Roll", 299, ""),

            # Wraps
            (categories["Wraps"], "Afghani Wrap", 529, ""),
            (categories["Wraps"], "Rapa Wrap", 609, ""),
            (categories["Wraps"], "Tortilla Crunch Warp", 519, ""),
            (categories["Wraps"], "Tortilla Grilled Warp", 519, ""),
            (categories["Wraps"], "Turkish Warp", 579, ""),

            # Sandwich
            (categories["Sandwich"], "Grilled Chicken Sandwich", 439, ""),
            (categories["Sandwich"], "Mexican Sandwich", 579, ""),
            (categories["Sandwich"], "Club Sandwich", 569, ""),

            # Coffee & Chai
            (categories["Coffee & Chai"], "Regular Tea", 120, ""),
            (categories["Coffee & Chai"], "Cardamom Tea", 130, ""),
            (categories["Coffee & Chai"], "Green Tea", 99, ""),

            # Dessert
            (categories["Dessert"], "Lava cake with ice cream", 419, ""),
            (categories["Dessert"], "Lava cake without ice cream", 359, ""),

            # Beverage
            (categories["Beverage"], "Soft Drink 1.5 Liter", 199, ""),
            (categories["Beverage"], "Soft Drink 1 Liter", 149, ""),
            (categories["Beverage"], "Mineral Water Large", 99, ""),
            (categories["Beverage"], "Mineral Water Small", 55, "")
        ]

        for category_id, name, price, description in menu_items:
            cursor.execute(
                "INSERT INTO menu_items (category_id, name, price, description) VALUES (?, ?, ?, ?)",
                (category_id, name, price, description)
            )

    conn.commit()
    conn.close()

# User operations
def authenticate_user(username, password):
    """Authenticate a user and return user details if successful."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, role FROM users WHERE username = ? AND password = ?",
                   (username, password))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return {"id": user[0], "username": username, "role": user[1]}
    return None

def get_all_users():
    """Get all users from the database."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, role FROM users ORDER BY username")
    users = cursor.fetchall()
    
    conn.close()
    return users

def add_user(username, password, role):
    """Add a new user to the database."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (username, password, role))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    
    conn.close()
    return success

def update_user(user_id, username, password=None, role=None):
    """Update an existing user in the database."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    try:
        if password:
            cursor.execute("""
                UPDATE users 
                SET username = ?, password = ?, role = ?
                WHERE id = ?
            """, (username, password, role, user_id))
        else:
            cursor.execute("""
                UPDATE users 
                SET username = ?, role = ?
                WHERE id = ?
            """, (username, role, user_id))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    
    conn.close()
    return success

def delete_user(user_id):
    """Delete a user from the database."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    
    conn.close()
    return success

# Category operations
def get_all_categories():
    """Get all categories from the database."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM categories ORDER BY name")
    categories = cursor.fetchall()
    
    conn.close()
    return categories

def get_category_names():
    """Get all category names from the database."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM categories ORDER BY name")
    categories = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return categories

def add_category(name):
    """Add a new category to the database."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    
    conn.close()
    return success

def update_category(category_id, name):
    """Update an existing category in the database."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE categories SET name = ? WHERE id = ?", (name, category_id))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    
    conn.close()
    return success

def delete_category(category_id):
    """Delete a category from the database."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    
    conn.close()
    return success

# Menu item operations
def get_menu_items_by_category(category_name):
    """Get menu items for a specific category."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.id, m.name, m.price, m.description 
        FROM menu_items m
        JOIN categories c ON m.category_id = c.id
        WHERE c.name = ?
        ORDER BY m.name
    """, (category_name,))
    
    menu_items = cursor.fetchall()
    
    conn.close()
    return menu_items

def get_menu_items_by_category_id(category_id):
    """Get menu items for a specific category ID."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, price, description 
        FROM menu_items
        WHERE category_id = ?
        ORDER BY name
    """, (category_id,))
    
    menu_items = cursor.fetchall()
    
    conn.close()
    return menu_items

def search_menu_items(search_term):
    """Search for menu items by name."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.id, m.name, m.price, m.description 
        FROM menu_items m
        WHERE LOWER(m.name) LIKE ?
        ORDER BY m.name
    """, (f"%{search_term.lower()}%",))
    
    menu_items = cursor.fetchall()
    
    conn.close()
    return menu_items

def add_menu_item(category_id, name, price, description):
    """Add a new menu item to the database."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO menu_items (category_id, name, price, description)
            VALUES (?, ?, ?, ?)
        """, (category_id, name, price, description))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    
    conn.close()
    return success

def update_menu_item(item_id, name, price, description):
    """Update an existing menu item in the database."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE menu_items 
            SET name = ?, price = ?, description = ?
            WHERE id = ?
        """, (name, price, description, item_id))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    
    conn.close()
    return success

def delete_menu_item(item_id):
    """Delete a menu item from the database."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM menu_items WHERE id = ?", (item_id,))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    
    conn.close()
    return success

def get_total_menu_items_count():
    """Get the total count of menu items."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM menu_items")
    count = cursor.fetchone()[0]
    
    conn.close()
    return count

# Bill operations
def get_todays_sales():
    """Get the total sales for today."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT SUM(total_amount) FROM bills WHERE date LIKE ?", (f"{today}%",))
    sales = cursor.fetchone()[0]
    
    conn.close()
    return sales if sales else 0

def get_recent_bills(limit=5):
    """Get the most recent bills."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, customer_name, total_amount, date 
        FROM bills 
        ORDER BY id DESC LIMIT ?
    """, (limit,))
    
    bills = cursor.fetchall()
    
    conn.close()
    return bills

def create_bill(customer_name, total_amount, user_id, bill_items):
    """Create a new bill with its items."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    try:
        # Insert bill
        cursor.execute("""
            INSERT INTO bills (customer_name, total_amount, date, user_id)
            VALUES (?, ?, ?, ?)
        """, (customer_name, total_amount, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              user_id))
        
        bill_id = cursor.lastrowid
        
        # Insert bill items
        for item in bill_items:
            item_id, quantity, price = item
            cursor.execute("""
                INSERT INTO bill_items (bill_id, item_id, quantity, price)
                VALUES (?, ?, ?, ?)
            """, (bill_id, item_id, quantity, price))
        
        conn.commit()
        success = bill_id
    except sqlite3.Error:
        success = False
    
    conn.close()
    return success

def get_bill_items(bill_id):
    """Get items for a specific bill."""
    conn = sqlite3.connect('chai_and_grill.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.name, bi.quantity, bi.price, (bi.quantity * bi.price) as total
        FROM bill_items bi
        JOIN menu_items m ON bi.item_id = m.id
        WHERE bi.bill_id = ?
    """, (bill_id,))
    
    items = cursor.fetchall()
    
    conn.close()
    return items