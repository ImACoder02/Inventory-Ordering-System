import tkinter as tk
from tkinter import messagebox

# Inventory App
class InventoryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Inventory Management")

        self.label = tk.Label(self.master, text="Welcome to the Inventory App!", font=("Arial", 16))
        self.label.pack(pady=20)

        self.add_item_button = tk.Button(self.master, text="Add Item", command=self.add_item)
        self.add_item_button.pack(pady=5)

        self.view_items_button = tk.Button(self.master, text="View Items", command=self.view_items)
        self.view_items_button.pack(pady=5)

        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.quit)
        self.exit_button.pack(pady=20)

    def add_item(self):
        messagebox.showinfo("Add Item", "Feature to add an item coming soon!")

    def view_items(self):
        messagebox.showinfo("View Items", "Feature to view items coming soon!")

# Admin Login
class AdminLogin:
    def __init__(self, master):
        self.master = master
        self.master.title("Admin Login")

        self.label = tk.Label(self.master, text="Admin Login", font=("Arial", 16))
        self.label.pack(pady=10)

        self.username_label = tk.Label(self.master, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.quit)
        self.exit_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Hardcoded admin credentials
        if username == "admin" and password == "admin123":
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.master.destroy()
            self.open_inventory_app()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_inventory_app(self):
        inventory_window = tk.Tk()
        InventoryApp(inventory_window)
        inventory_window.mainloop()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    AdminLogin(root)
    root.mainloop()
