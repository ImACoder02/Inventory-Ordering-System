import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',  # Change as needed
                user='root',       # Your database username
                password='',       # Your database password
                database='inventory_management'  # Database name
            )
            if self.connection.is_connected():
                print("Connected to MySQL Database")
        except Error as e:
            print(f"Error: {e}")
            raise
    # Inventory Management
    def add_product(self, product_name, category, price, stock_quantity):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO products (product_name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (product_name, category, price, stock_quantity))
            self.connection.commit()
        except Error as e:
            print(f"Error: {e}")
            raise

    def fetch_products(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM products"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            raise

    def update_product(self, product_id, product_name, category, price, stock_quantity):
        try:
            cursor = self.connection.cursor()
            query = """UPDATE products SET product_name=%s, category=%s, price=%s, stock_quantity=%s WHERE product_id=%s"""
            cursor.execute(query, (product_name, category, price, stock_quantity, product_id))
            self.connection.commit()
        except Error as e:
            print(f"Error: {e}")
            raise
    
    def delete_product(self, product_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM products WHERE product_id=%s"
            cursor.execute(query, (product_id,))
            self.connection.commit()
        except Error as e:
            print(f"Error: {e}")
            raise

    def search_products(self, search_term=None, category=None, min_price=None, max_price=None):
        try:
            cursor = self.connection.cursor()
            base_query = "SELECT * FROM products WHERE 1=1"  # Dummy condition to simplify query-building
            conditions = []
            params = []

            # Add conditions based on provided parameters
            if search_term:
                conditions.append("product_name LIKE %s")
                params.append(f"%{search_term}%")
            if category:
                conditions.append("category = %s")
                params.append(category)
            if min_price is not None:  # If minimum price is provided
                conditions.append("price >= %s")
                params.append(min_price)
            if max_price is not None:  # If maximum price is provided
                conditions.append("price <= %s")
                params.append(max_price)

            # Combine the base query with conditions
            if conditions:
                base_query += " AND " + " AND ".join(conditions)

            # Execute the query
            cursor.execute(base_query, tuple(params))
            return cursor.fetchall()

        except Error as e:
            print(f"Error: {e}")
            raise

     # Admin & User Account management
    def create_admin(self, username, password):
        try:
            cursor = self.connection.cursor()
            # Check if username exists in either table
            check_query = "SELECT username FROM admins WHERE username = %s UNION SELECT username FROM users WHERE username = %s"
            cursor.execute(check_query, (username, username))
            if cursor.fetchone():
                print("Username already exists.")
                return False

            query = "INSERT INTO admins (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False

    def create_user(self, username, password):
        try:
            cursor = self.connection.cursor()
            # Check if username exists in either table
            check_query = "SELECT username FROM users WHERE username = %s UNION SELECT username FROM admins WHERE username = %s"
            cursor.execute(check_query, (username, username))
            if cursor.fetchone():
                print("Username already exists.")
                return False

            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False

    def verify_admin(self, username, password):
        try:
            cursor = self.connection.cursor()
            query = "SELECT username, password FROM admins WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            return cursor.fetchone() is not None
        except Error as e:
            print(f"Error: {e}")
            return False

    def verify_user(self, username, password):
        try:
            cursor = self.connection.cursor()
            query = "SELECT username, password FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            return cursor.fetchone() is not None
        except Error as e:
            print(f"Error: {e}")
            return False

# Ordering System







