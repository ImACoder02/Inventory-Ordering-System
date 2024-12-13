import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import messagebox, ttk
from backend.db import Database
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1920x1080")  # Set the width to 1440 and height to 1024
        self.root.resizable(True, True)  # Optional: Disable 
        self.root.configure(bg="#808080")
        self.db = Database()

        # Header Frame
        self.header_frame = tk.Frame(self.root, bg="#213A58", height=80)
        self.header_frame.pack(side="top", fill="x")  # Position at the top, full width
        self.header_frame.pack_propagate(False)  # Prevent resizing based on contents

        # Add a label inside the header frame
        header_label = tk.Label(
            self.header_frame, 
            text="INVENTORY MANAGEMENT SYSTEM", 
            bg="#213A58", 
            fg="white", 
            font=("Arial", 23, "bold")
        )
        header_label.pack(pady=20)


        # Input Frame
        self.header_input_frame = tk.Frame(self.root, bg="white", width=1480, height=650)
        self.header_input_frame.place(relx=0.5, rely=0.5, y=40, anchor="center")
        self.header_input_frame.pack_propagate(False)

        # UI Components
        self.product_name_label = tk.Label(self.header_input_frame, bg="white", font=("Arial", 15), text="Product Name")
        self.product_name_label.place(x=40, y=50, anchor="nw")
        self.product_name_entry = tk.Entry(self.header_input_frame, font=("Arial", 15), bg="#D9D9D9", width=27)
        self.product_name_entry.place(x=300, y=53, anchor="nw")

        self.category_label = tk.Label(self.header_input_frame, bg="white", font=("Arial", 15), text="Category")
        self.category_label.place(x=55, y=110, anchor="nw")
        self.category_combobox = ttk.Combobox(self.header_input_frame, values=["Food", "Drinks", "Clothing", "Electronics"], font=("Arial", 15), state="readonly")
        self.category_combobox.place(x=300, y=113, anchor="nw")
        self.category_combobox.set("Food")  # Default category selection

        self.price_label = tk.Label(self.header_input_frame, bg="white", font=("Arial", 15), text="Price")
        self.price_label.place(x=70, y=170, anchor="nw")
        self.price_entry = tk.Entry(self.header_input_frame, font=("Arial", 15), bg="#D9D9D9", width=27)
        self.price_entry.place(x=300, y=173, anchor="nw")

        self.stock_quantity_label = tk.Label(self.header_input_frame, bg="white", font=("Arial", 15), text="Stock Quantity")
        self.stock_quantity_label.place(x=40, y=230, anchor="nw")
        self.stock_quantity_entry = tk.Entry(self.header_input_frame, font=("Arial", 15), bg="#D9D9D9", width=27)
        self.stock_quantity_entry.place(x=300, y=233, anchor="nw")

        # Label and Entry for search field
        self.search_label = tk.Label(self.header_input_frame, bg="white", font=("Arial", 15), text="Search By:")
        self.search_label.place(x=800, y=50, anchor="nw")
        self.search_entry = tk.Entry(self.header_input_frame, font=("Arial", 15), bg="#D9D9D9", width=22)
        self.search_entry.place(x=910, y=85, anchor="nw")

        
        # ComboBox for selecting search field (Product Name, Category, Price)
        self.search_field_combobox = ttk.Combobox(self.header_input_frame, values=["Product Name", "Category", "Price"], font=("Arial", 15))
        self.search_field_combobox.place(x=910, y=50, anchor="nw")  # Position combo box to the right of the label
        self.search_field_combobox.set("Product Name")  # Default selection
        
        

        # Buttons and Listbox
        self.listbox_frame = tk.Frame(self.header_input_frame, bg="#D9D9D9", width=1400, height=325)
        self.listbox_frame.place(relx=0.5, rely=0.5, y=130, anchor="center")
        self.listbox_frame.pack_propagate(False)

        self.button_frame = tk.Frame(self.listbox_frame, bg="#D9D9D9")
        self.button_frame.pack(side="top", pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add Product", command=self.add_product)
        self.add_button.grid(row=0, column=0, padx=10)

        self.update_button = tk.Button(self.button_frame, text="Update Product", command=self.update_product)
        self.update_button.grid(row=0, column=1, padx=10)

        self.delete_button = tk.Button(self.button_frame, text="Delete Product", command=self.delete_product)
        self.delete_button.grid(row=0, column=2, padx=10)

        self.view_button = tk.Button(self.button_frame, text="View Inventory", command=self.view_inventory)
        self.view_button.grid(row=0, column=3, padx=10)

        self.search_button = tk.Button(self.button_frame, text="Search", command=self.search_products)
        self.search_button.grid(row=0, column=4, padx=10)

        self.product_listbox = tk.Listbox(self.listbox_frame, font=("Arial", 12), bg="white", height=14, width=150)
        self.product_listbox.place(relx=0.5, rely=0.5, y=10, anchor="center")

        # Listbox to display products
        self.product_listbox = tk.Listbox(self.listbox_frame, font=("Arial", 12), bg="white", height=14, width=150)
        self.product_listbox.place(relx=0.5, rely=0.5, y=10, anchor="center")  
    
    
    
    def add_product(self):
        product_name = self.product_name_entry.get()
        category = self.category_combobox.get()
        try:
            price = float(self.price_entry.get())
            stock_quantity = int(self.stock_quantity_entry.get())
            product_id = self.db.add_product(product_name, category, price, stock_quantity)
            messagebox.showinfo("Success", "Product added successfully!")
            self.view_inventory()  # Refresh the inventory list after adding the product
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid price and quantity.")

    def update_product(self):
        try:
            selected_item = self.product_listbox.curselection()
            if selected_item:
                # Extract the product ID from the selected item
                product_text = self.product_listbox.get(selected_item)
                product_id = int(product_text.split(",")[0].split(":")[1].strip())  # Parse ID from text
                
                # Get updated product details from the entries
                product_name = self.product_name_entry.get()
                category = self.category_combobox.get()
                price = float(self.price_entry.get())
                stock_quantity = int(self.stock_quantity_entry.get())
                
                # Call the database update method
                self.db.update_product(product_id, product_name, category, price, stock_quantity)
                messagebox.showinfo("Success", "Product updated successfully!")
                
                # Refresh the Listbox to reflect changes
                self.view_inventory()
            else:
                messagebox.showerror("No Selection", "Please select a product to update.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid price and quantity.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during update: {e}")


    def delete_product(self):
        try:
            selected_item = self.product_listbox.curselection()
            if selected_item:
                # Extract the product ID from the selected item
                product_text = self.product_listbox.get(selected_item)
                product_id = int(product_text.split(",")[0].split(":")[1].strip())  # Parse ID from text
                
                # Call the database delete method
                self.db.delete_product(product_id)
                messagebox.showinfo("Success", "Product deleted successfully!")
                
                # Refresh the Listbox to reflect changes
                self.view_inventory()
            else:
                messagebox.showerror("No Selection", "Please select a product to delete.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during deletion: {e}")

    def search_products(self):
        # Get the search inputs from the user
        search_field = self.search_field_combobox.get()  # Retrieve the selected search field
        search_term = self.search_entry.get().strip()  # Search term from the entry field
        category = None  # Default is None for category
        price = None  # Default is None for price

        # Initialize search parameters based on the selected search field
        if search_field == "Product Name":
            # Use the search term entered in the search field
            search_term = self.search_entry.get().strip()
        elif search_field == "Category":
            # Use the search term entered in the search field as the category
            category = search_term
            search_term = None  # Set search term to None for category search
        elif search_field == "Price":
            # Ensure the price is a valid number, then use it
            if search_term and search_term.replace('.', '', 1).isdigit():
                price = float(search_term)
                search_term = None  # Set search term to None for price search
            else:
                messagebox.showerror("Input Error", "Please enter a valid price.")
                return

        # Validate that at least one field is filled
        if not search_term and not category and not price:
            messagebox.showerror("Input Error", "Please enter a search term in at least one field.")
            return

        try:
            # Query the database for matching products
            results = self.db.search_products(search_term=search_term, category=category, min_price=price, max_price=price)
            
            if results:
                # Clear the listbox before displaying the new search results
                self.product_listbox.delete(0, tk.END)
                
                # Insert the results into the listbox
                for product in results:
                    self.product_listbox.insert(
                        tk.END,
                        f"ID: {product[0]}, Name: {product[1]}, Category: {product[2]}, Price: ${product[3]:.2f}, Stock: {product[4]}"
                    )
            else:
                messagebox.showinfo("No Results", "No products found matching your search.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during the search: {e}")



    def view_inventory(self):
        inventory = self.db.fetch_products()
        self.product_listbox.delete(0, tk.END)  # Clear previous list
        for product in inventory:
            self.product_listbox.insert(tk.END, f"ID: {product[0]}, Name: {product[1]}, Category: {product[2]}, Price: ${product[3]:.2f}, Stock: {product[4]}")

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("444x607")
        self.root.resizable(False, False)
        self.db = Database()  # Replace with your Database class instance
        
        # Load an image using Pillow
        try:
            self.image = Image.open("image.png")  # Replace with your image file path
            self.image_resized = self.image.resize((130, 130))  # Resize to 130x130 pixels
            self.image_tk = ImageTk.PhotoImage(self.image_resized)
            self.label = tk.Label(self.root, image=self.image_tk)
            self.label.pack(padx=20, pady=0)
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading image: {e}")
        
        # Create a welcome label
        tk.Label(self.root, text="Welcome to StockFlow", font=("Arial", 20, "bold")).place(x=65, y=120)

        # Username Label and Entry
        tk.Label(self.root, text="Username", font=("Arial", 12)).place(x=64, y=180)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=35)
        self.username_entry.place(x=65, y=200)
        
        # Password Label and Entry
        tk.Label(self.root, text="Password", font=("Arial", 12)).place(x=64, y=240)
        self.password_entry = tk.Entry(self.root, font=("Arial", 12), width=35, show="*")
        self.password_entry.place(x=65, y=260)

        # Login Button
        tk.Button(self.root, text="Log In", font=("Arial", 12), width=33, height=2,
                  bg="#213A58", fg="#FFFFFF", command=self.user_login).place(x=70, y=300)

        # Sign-Up Button
        tk.Button(self.root, text="Sign Up", font=("Arial", 12), width=33, height=2,
                  bg="#213A58", fg="#FFFFFF", command=self.show_signup_window).place(x=70, y=360)

        # OR Label
        tk.Label(self.root, text="OR", font=("Arial", 12, "bold")).place(x=210, y=420)

        # Admin Login Button
        tk.Button(self.root, text="Log In As Admin", font=("Arial", 12), width=33, height=2,
                  bg="#213A58", fg="#FFFFFF", command=self.admin_login).place(x=70, y=450)

    def user_login(self):
        # Retrieve the entered username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Here, replace this with the actual authentication logic
        if self.db.verify_user(username, password):  # Assuming the 'verify_admin' method checks admin credentials
            messagebox.showinfo("Login Successful", "Welcome User!")
            self.root.destroy()  # Close the login window
            self.open_ordering_app()  # Open the InventoryApp
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    def admin_login(self):
        # Retrieve the entered username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Here, replace this with the actual authentication logic
        if self.db.verify_admin(username, password):  # Assuming the 'verify_admin' method checks admin credentials
            messagebox.showinfo("Login Successful", "Welcome Admin!")
            self.root.destroy()  # Close the login window
            self.open_inventory_app()  # Open the InventoryApp
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    def open_inventory_app(self):
        inventory_root = tk.Tk()  # Create a new root window for the InventoryApp
        app = InventoryApp(inventory_root)  # Initialize the InventoryApp with the new root
        inventory_root.mainloop()  # Start the Tkinter event loop for the InventoryApp

    def open_ordering_app(self):
        inventory_root = tk.Tk()  # Create a new root window for the InventoryApp
        app = OrderingSystem(inventory_root)  # Initialize the InventoryApp with the new root
        inventory_root.mainloop()  # Start the Tkinter event loop for the InventoryApp

    def register_user(self, username, password):
        if not username or not password:
            messagebox.showerror("Input Error", "Please enter both username and password.")
            return

        if self.db.create_user(username, password):
            messagebox.showinfo("Success", "User registered successfully!")
        else:
            messagebox.showerror("Error", "Registration failed. Username might already exist.")

    def register_admin(self, username, password):
        if not username or not password:
            messagebox.showerror("Input Error", "Please enter both username and password.")
            return

        if self.db.create_admin(username, password):
            messagebox.showinfo("Success", "Admin registered successfully!")
        else:
            messagebox.showerror("Error", "Registration failed. Username might already exist.")

    def show_signup_window(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Sign Up")
        signup_window.geometry("400x300")
        
        # Title label
        tk.Label(signup_window, text="Sign Up to StockFlow", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Username label and entry
        tk.Label(signup_window, text="Username:", font=("Arial", 12)).pack(pady=5)
        username_entry = tk.Entry(signup_window, font=("Arial", 12))
        username_entry.pack(pady=5)
        
        # Password label and entry
        tk.Label(signup_window, text="Password:", font=("Arial", 12)).pack(pady=5)
        password_entry = tk.Entry(signup_window, font=("Arial", 12), show="*")
        password_entry.pack(pady=5)
        
        # Register buttons with color styling
        button_color = "#213A58"
        text_color = "white"
        
        tk.Button(signup_window, text="Register As User", font=("Arial", 12), 
                  command=lambda: self.register_user(username_entry.get(), password_entry.get()),
                  bg=button_color, fg=text_color).pack(pady=10, fill='x', padx=20)
        
        tk.Button(signup_window, text="Register As Admin", font=("Arial", 12), 
                  command=lambda: self.register_admin(username_entry.get(), password_entry.get()),
                  bg=button_color, fg=text_color).pack(pady=10, fill='x', padx=20)
        
# Ordering System
class OrderingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Ordering System")
        self.root.geometry("1280x720")
        self.root.configure(bg="#FFFFFF")

        # Sidebar Frame
        self.sidebar_frame = tk.Frame(self.root, bg="#213A58", width=300, height=720)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        # Sidebar Label
        sidebar_label = tk.Label(
            self.sidebar_frame,
            text="FLOWSTACK",
            font=("Arial", 24, "bold"),
            fg="#FFFFFF",
            bg="#213A58",
            anchor="center"
        )
        sidebar_label.place(relx=0.5, rely=0.1, anchor="center")

        # Category Buttons
        self.categories = ["FOOD", "DRINKS", "CLOTHING", "ELECTRONICS"]
        self.buttons = {}

        for idx, category in enumerate(self.categories):
            button = tk.Button(
                self.sidebar_frame,
                text=category,
                font=("Arial", 12),
                bg="#D3D3D3",
                fg="#213A58",
                width=25,
                command=lambda c=category: self.display_products(c)
            )
            button.place(relx=0.5, rely=(0.2 + idx * 0.1), anchor="center")
            self.buttons[category] = button

        # Main Frame
        self.main_frame = tk.Frame(self.root, bg="#FFFFFF", width=980, height=620)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Product Table Label
        self.product_label = tk.Label(
            self.main_frame,
            text="Available Products",
            font=("Arial", 16, "bold"),
            bg="#FFFFFF",
            anchor="w"
        )
        self.product_label.pack(pady=10)

         # Treeview for Product Details
        self.product_tree = ttk.Treeview(
            self.main_frame,
            columns=("Product Name", "Price", "Quantity"),
            show="headings",
            height=10  # Reduced height for smaller display
        )
        self.product_tree.pack(pady=10, padx=10, fill="x", expand=False)

        # Define Columns
        self.product_tree.heading("Product Name", text="Product Name")
        self.product_tree.heading("Price", text="Price")
        self.product_tree.heading("Quantity", text="Quantity")
        self.product_tree.column("Product Name", width=300, anchor="center")
        self.product_tree.column("Price", width=100, anchor="center")
        self.product_tree.column("Quantity", width=100, anchor="center")

        # Sample Inventory
        self.inventory = {
            "FOOD": [("Burger", 5.00, 10), ("Pizza", 8.50, 5), ("Pasta", 7.00, 12)],
            "DRINKS": [("Soda", 1.50, 30), ("Coffee", 2.00, 15), ("Tea", 1.25, 20)],
            "CLOTHING": [("Shirt", 15.00, 50), ("Pants", 20.00, 40), ("Jacket", 50.00, 10)],
            "ELECTRONICS": [("Phone", 500.00, 8), ("Laptop", 1200.00, 5), ("Headphones", 75.00, 25)]
        }

    def display_products(self, category):
        """Displays the products for the selected category."""
        # Clear the treeview
        for row in self.product_tree.get_children():
            self.product_tree.delete(row)

        # Fetch products and insert them into the treeview
        products = self.inventory.get(category, [])
        for product in products:
            self.product_tree.insert("", "end", values=product)


if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()






