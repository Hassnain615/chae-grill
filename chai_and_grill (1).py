import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import os
import datetime
from PIL import Image, ImageTk
import tempfile
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as ReportLabImage
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import csv
import io

# Import database operations
import database_operations as db


class ChaiAndGrillApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chai & Grill Restaurant Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#000000")
        self.root.resizable(True, True)

        # Set icon
        self.logo_img = tk.PhotoImage(file="logo.png")
        self.root.iconphoto(False, self.logo_img)

        # Initialize database
        db.create_database()

        # Variables
        self.current_user = None
        self.cart = []
        self.selected_category = tk.StringVar()
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.search_menu)

        # Create frames
        self.create_frames()

        # Start with login screen
        self.show_login()

    def create_frames(self):
        # Main container frame
        self.container = tk.Frame(self.root, bg="#000000")
        self.container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Login frame
        self.login_frame = tk.Frame(self.container, bg="#000000")

        # Main application frame
        self.main_frame = tk.Frame(self.container, bg="#000000")

        # Dashboard frame
        self.dashboard_frame = tk.Frame(self.main_frame, bg="#000000")

        # Billing frame
        self.billing_frame = tk.Frame(self.main_frame, bg="#000000")

        # Menu management frame
        self.menu_mgmt_frame = tk.Frame(self.main_frame, bg="#000000")

        # User management frame
        self.user_mgmt_frame = tk.Frame(self.main_frame, bg="#000000")

    def show_login(self):
        # Hide all frames
        for frame in [self.main_frame, self.login_frame]:
            frame.pack_forget()

        # Configure login frame
        self.login_frame = tk.Frame(self.container, bg="#000000")
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        # Logo
        logo_frame = tk.Frame(self.login_frame, bg="#000000")
        logo_frame.pack(pady=20)

        logo_img = Image.open("logo.png")
        logo_img = logo_img.resize((200, 200), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)

        logo_label = tk.Label(logo_frame, image=logo_photo, bg="#000000")
        logo_label.image = logo_photo
        logo_label.pack()

        # Login form
        form_frame = tk.Frame(self.login_frame, bg="#FFC107", bd=2)
        form_frame.pack(pady=20, padx=50, fill=tk.X)

        title_label = tk.Label(form_frame, text="Chai & Grill Management System",
                               font=("Arial", 18, "bold"), bg="#FFC107", fg="#000000")
        title_label.pack(pady=10)

        username_frame = tk.Frame(form_frame, bg="#FFC107")
        username_frame.pack(pady=10, padx=20, fill=tk.X)

        username_label = tk.Label(username_frame, text="Username:",
                                  font=("Arial", 12), bg="#FFC107", fg="#000000")
        username_label.pack(side=tk.LEFT, padx=5)

        self.username_entry = tk.Entry(username_frame, font=("Arial", 12), bd=2)
        self.username_entry.pack(side=tk.RIGHT, padx=5, expand=True, fill=tk.X)

        password_frame = tk.Frame(form_frame, bg="#FFC107")
        password_frame.pack(pady=10, padx=20, fill=tk.X)

        password_label = tk.Label(password_frame, text="Password:",
                                  font=("Arial", 12), bg="#FFC107", fg="#000000")
        password_label.pack(side=tk.LEFT, padx=5)

        self.password_entry = tk.Entry(password_frame, font=("Arial", 12), bd=2, show="*")
        self.password_entry.pack(side=tk.RIGHT, padx=5, expand=True, fill=tk.X)

        button_frame = tk.Frame(form_frame, bg="#FFC107")
        button_frame.pack(pady=20)

        login_button = tk.Button(button_frame, text="Login", font=("Arial", 12, "bold"),
                                 bg="#000000", fg="#FFC107", padx=20, pady=5,
                                 command=self.login)
        login_button.pack()

        # Version info
        version_label = tk.Label(self.login_frame, text="Version 1.0",
                                 font=("Arial", 8), bg="#000000", fg="#FFFFFF")
        version_label.pack(side=tk.BOTTOM, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        user = db.authenticate_user(username, password)

        if user:
            self.current_user = user
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show_dashboard(self):
        # Hide all frames
        for frame in [self.main_frame, self.login_frame]:
            frame.pack_forget()

        # Configure main frame
        self.main_frame = tk.Frame(self.container, bg="#000000")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create header
        self.create_header()

        # Create sidebar
        self.create_sidebar()

        # Create dashboard content
        self.dashboard_frame = tk.Frame(self.main_frame, bg="#000000")
        self.dashboard_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Dashboard title
        title_frame = tk.Frame(self.dashboard_frame, bg="#FFC107")
        title_frame.pack(fill=tk.X, pady=10)

        title_label = tk.Label(title_frame, text="Dashboard", font=("Arial", 16, "bold"),
                               bg="#FFC107", fg="#000000", padx=10, pady=5)
        title_label.pack(side=tk.LEFT)

        date_label = tk.Label(title_frame, text=datetime.datetime.now().strftime("%d-%m-%Y"),
                              font=("Arial", 12), bg="#FFC107", fg="#000000", padx=10)
        date_label.pack(side=tk.RIGHT)

        # Dashboard widgets
        widgets_frame = tk.Frame(self.dashboard_frame, bg="#000000")
        widgets_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Configure grid
        widgets_frame.columnconfigure(0, weight=1)
        widgets_frame.columnconfigure(1, weight=1)
        widgets_frame.rowconfigure(0, weight=1)
        widgets_frame.rowconfigure(1, weight=1)

        # Today's sales widget
        sales_frame = tk.Frame(widgets_frame, bg="#FFC107", bd=2)
        sales_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        sales_title = tk.Label(sales_frame, text="Today's Sales", font=("Arial", 14, "bold"),
                               bg="#FFC107", fg="#000000", padx=10, pady=5)
        sales_title.pack(fill=tk.X)

        # Get today's sales from database
        today_sales = db.get_todays_sales()

        sales_amount = tk.Label(sales_frame, text=f"Rs. {today_sales:.2f}",
                                font=("Arial", 24, "bold"), bg="#FFC107", fg="#000000", pady=20)
        sales_amount.pack()

        # Total menu items widget
        items_frame = tk.Frame(widgets_frame, bg="#FFC107", bd=2)
        items_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        items_title = tk.Label(items_frame, text="Total Menu Items", font=("Arial", 14, "bold"),
                               bg="#FFC107", fg="#000000", padx=10, pady=5)
        items_title.pack(fill=tk.X)

        # Get total menu items from database
        total_items = db.get_total_menu_items_count()

        items_count = tk.Label(items_frame, text=str(total_items),
                               font=("Arial", 24, "bold"), bg="#FFC107", fg="#000000", pady=20)
        items_count.pack()

        # Recent bills widget
        bills_frame = tk.Frame(widgets_frame, bg="#FFC107", bd=2)
        bills_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        bills_title = tk.Label(bills_frame, text="Recent Bills", font=("Arial", 14, "bold"),
                               bg="#FFC107", fg="#000000", padx=10, pady=5)
        bills_title.pack(fill=tk.X)

        # Create treeview for recent bills
        columns = ("Bill ID", "Customer", "Amount", "Date")
        bills_tree = ttk.Treeview(bills_frame, columns=columns, show="headings", height=5)

        for col in columns:
            bills_tree.heading(col, text=col)
            bills_tree.column(col, width=100)

        bills_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Get recent bills from database
        recent_bills = db.get_recent_bills()

        for bill in recent_bills:
            bills_tree.insert("", "end", values=bill)

    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg="#FFC107", height=60)
        header_frame.pack(side=tk.TOP, fill=tk.X)

        # Logo
        logo_img = Image.open("logo.png")
        logo_img = logo_img.resize((50, 50), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)

        logo_label = tk.Label(header_frame, image=logo_photo, bg="#FFC107")
        logo_label.image = logo_photo
        logo_label.pack(side=tk.LEFT, padx=10)

        # Title
        title_label = tk.Label(header_frame, text="Chai & Grill Management System",
                               font=("Arial", 16, "bold"), bg="#FFC107", fg="#000000")
        title_label.pack(side=tk.LEFT, padx=10)

        # User info
        user_frame = tk.Frame(header_frame, bg="#FFC107")
        user_frame.pack(side=tk.RIGHT, padx=10)

        user_label = tk.Label(user_frame, text=f"User: {self.current_user['username']}",
                              font=("Arial", 12), bg="#FFC107", fg="#000000")
        user_label.pack(side=tk.LEFT, padx=5)

        logout_button = tk.Button(user_frame, text="Logout", font=("Arial", 10),
                                  bg="#000000", fg="#FFC107", command=self.logout)
        logout_button.pack(side=tk.LEFT, padx=5)

    def create_sidebar(self):
        sidebar_frame = tk.Frame(self.main_frame, bg="#FFC107", width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Ensure the sidebar maintains its width
        sidebar_frame.pack_propagate(False)

        # Menu buttons
        dashboard_btn = tk.Button(sidebar_frame, text="Dashboard", font=("Arial", 12),
                                  bg="#000000", fg="#FFC107", padx=10, pady=5,
                                  command=self.show_dashboard)
        dashboard_btn.pack(fill=tk.X, pady=5)

        billing_btn = tk.Button(sidebar_frame, text="Billing", font=("Arial", 12),
                                bg="#000000", fg="#FFC107", padx=10, pady=5,
                                command=self.show_billing)
        billing_btn.pack(fill=tk.X, pady=5)

        menu_btn = tk.Button(sidebar_frame, text="Menu Management", font=("Arial", 12),
                             bg="#000000", fg="#FFC107", padx=10, pady=5,
                             command=self.show_menu_management)
        menu_btn.pack(fill=tk.X, pady=5)

        # Only show user management for admin users
        if self.current_user["role"] == "admin":
            user_btn = tk.Button(sidebar_frame, text="User Management", font=("Arial", 12),
                                 bg="#000000", fg="#FFC107", padx=10, pady=5,
                                 command=self.show_user_management)
            user_btn.pack(fill=tk.X, pady=5)

    def logout(self):
        self.current_user = None
        self.show_login()

    def show_billing(self):
        # Clear main content area
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        # Configure billing frame
        self.billing_frame = tk.Frame(self.dashboard_frame, bg="#000000")
        self.billing_frame.pack(fill=tk.BOTH, expand=True)

        # Billing title
        title_frame = tk.Frame(self.billing_frame, bg="#FFC107")
        title_frame.pack(fill=tk.X, pady=10)

        title_label = tk.Label(title_frame, text="Billing", font=("Arial", 16, "bold"),
                               bg="#FFC107", fg="#000000", padx=10, pady=5)
        title_label.pack(side=tk.LEFT)

        # Main billing area
        billing_area = tk.Frame(self.billing_frame, bg="#000000")
        billing_area.pack(fill=tk.BOTH, expand=True, pady=10)

        # Split into left and right panels
        left_panel = tk.Frame(billing_area, bg="#000000", width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)

        right_panel = tk.Frame(billing_area, bg="#000000")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Left panel - Menu selection
        menu_frame = tk.Frame(left_panel, bg="#FFC107")
        menu_frame.pack(fill=tk.BOTH, expand=True)

        # Category selection
        category_frame = tk.Frame(menu_frame, bg="#FFC107")
        category_frame.pack(fill=tk.X, padx=10, pady=10)

        category_label = tk.Label(category_frame, text="Category:",
                                  font=("Arial", 12), bg="#FFC107", fg="#000000")
        category_label.pack(side=tk.LEFT, padx=5)

        # Get categories from database
        categories = db.get_category_names()

        category_dropdown = ttk.Combobox(category_frame, textvariable=self.selected_category,
                                         values=categories, state="readonly", width=20)
        category_dropdown.pack(side=tk.LEFT, padx=5)
        category_dropdown.bind("<<ComboboxSelected>>", self.load_menu_items)

        # Search box
        search_frame = tk.Frame(menu_frame, bg="#FFC107")
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        search_label = tk.Label(search_frame, text="Search:",
                                font=("Arial", 12), bg="#FFC107", fg="#000000")
        search_label.pack(side=tk.LEFT, padx=5)

        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Menu items list
        menu_list_frame = tk.Frame(menu_frame, bg="#FFFFFF")
        menu_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("ID", "Name", "Price", "Description")
        self.menu_tree = ttk.Treeview(menu_list_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.menu_tree.heading(col, text=col)

        self.menu_tree.column("ID", width=50)
        self.menu_tree.column("Name", width=150)
        self.menu_tree.column("Price", width=80)
        self.menu_tree.column("Description", width=100)

        self.menu_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for menu tree
        menu_scrollbar = ttk.Scrollbar(menu_list_frame, orient="vertical", command=self.menu_tree.yview)
        menu_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.menu_tree.configure(yscrollcommand=menu_scrollbar.set)

        # Add to cart button
        add_btn = tk.Button(menu_frame, text="Add to Cart", font=("Arial", 12),
                            bg="#000000", fg="#FFC107", padx=10, pady=5,
                            command=self.add_to_cart)
        add_btn.pack(pady=10)

        # Right panel - Cart and billing
        cart_frame = tk.Frame(right_panel, bg="#FFC107")
        cart_frame.pack(fill=tk.BOTH, expand=True)

        # Customer info
        customer_frame = tk.Frame(cart_frame, bg="#FFC107")
        customer_frame.pack(fill=tk.X, padx=10, pady=10)

        customer_label = tk.Label(customer_frame, text="Customer Name:",
                                  font=("Arial", 12), bg="#FFC107", fg="#000000")
        customer_label.pack(side=tk.LEFT, padx=5)

        self.customer_entry = tk.Entry(customer_frame, width=30)
        self.customer_entry.pack(side=tk.LEFT, padx=5)

        # Cart items
        cart_list_frame = tk.Frame(cart_frame, bg="#FFFFFF")
        cart_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("ID", "Name", "Price", "Quantity", "Total")
        self.cart_tree = ttk.Treeview(cart_list_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.cart_tree.heading(col, text=col)

        self.cart_tree.column("ID", width=50)
        self.cart_tree.column("Name", width=150)
        self.cart_tree.column("Price", width=80)
        self.cart_tree.column("Quantity", width=80)
        self.cart_tree.column("Total", width=80)

        self.cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for cart tree
        cart_scrollbar = ttk.Scrollbar(cart_list_frame, orient="vertical", command=self.cart_tree.yview)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_tree.configure(yscrollcommand=cart_scrollbar.set)

        # Cart buttons
        cart_btn_frame = tk.Frame(cart_frame, bg="#FFC107")
        cart_btn_frame.pack(fill=tk.X, padx=10, pady=10)

        remove_btn = tk.Button(cart_btn_frame, text="Remove Item", font=("Arial", 12),
                               bg="#000000", fg="#FFC107", padx=10, pady=5,
                               command=self.remove_from_cart)
        remove_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = tk.Button(cart_btn_frame, text="Clear Cart", font=("Arial", 12),
                              bg="#000000", fg="#FFC107", padx=10, pady=5,
                              command=self.clear_cart)
        clear_btn.pack(side=tk.LEFT, padx=5)

        # Total and checkout
        total_frame = tk.Frame(cart_frame, bg="#FFC107")
        total_frame.pack(fill=tk.X, padx=10, pady=10)

        total_label = tk.Label(total_frame, text="Total Amount:",
                               font=("Arial", 14, "bold"), bg="#FFC107", fg="#000000")
        total_label.pack(side=tk.LEFT, padx=5)

        self.total_var = tk.StringVar()
        self.total_var.set("Rs. 0.00")

        total_amount = tk.Label(total_frame, textvariable=self.total_var,
                                font=("Arial", 14, "bold"), bg="#FFC107", fg="#000000")
        total_amount.pack(side=tk.LEFT, padx=5)

        # Checkout button
        checkout_btn = tk.Button(cart_frame, text="Generate Bill", font=("Arial", 14, "bold"),
                                 bg="#000000", fg="#FFC107", padx=20, pady=10,
                                 command=self.generate_bill)
        checkout_btn.pack(pady=10)

    def load_menu_items(self, event=None):
        category = self.selected_category.get()

        if not category:
            return

        # Clear existing items
        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)

        # Get menu items for selected category
        menu_items = db.get_menu_items_by_category(category)

        # Add items to treeview
        for item in menu_items:
            self.menu_tree.insert("", "end", values=item)

    def search_menu(self, *args):
        search_term = self.search_var.get()

        if not search_term:
            self.load_menu_items()
            return

        # Clear existing items
        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)

        # Search menu items
        menu_items = db.search_menu_items(search_term)

        # Add items to treeview
        for item in menu_items:
            self.menu_tree.insert("", "end", values=item)

    def add_to_cart(self):
        selected_item = self.menu_tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a menu item")
            return

        item_data = self.menu_tree.item(selected_item, "values")
        item_id = item_data[0]
        item_name = item_data[1]
        item_price = float(item_data[2])

        # Ask for quantity
        quantity = simpledialog.askinteger("Quantity", f"Enter quantity for {item_name}:",
                                           minvalue=1, maxvalue=100)

        if not quantity:
            return

        # Check if item already in cart
        for item in self.cart_tree.get_children():
            cart_item = self.cart_tree.item(item, "values")
            if cart_item[0] == item_id:
                # Update quantity
                new_quantity = int(cart_item[3]) + quantity
                new_total = new_quantity * item_price
                self.cart_tree.item(item, values=(item_id, item_name, item_price, new_quantity, new_total))
                self.update_total()
                return

        # Add new item to cart
        total = quantity * item_price
        self.cart_tree.insert("", "end", values=(item_id, item_name, item_price, quantity, total))

        # Update total
        self.update_total()

    def remove_from_cart(self):
        selected_item = self.cart_tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select an item to remove")
            return

        self.cart_tree.delete(selected_item)
        self.update_total()

    def clear_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        self.update_total()

    def update_total(self):
        total = 0

        for item in self.cart_tree.get_children():
            item_data = self.cart_tree.item(item, "values")
            total += float(item_data[4])

        self.total_var.set(f"Rs. {total:.2f}")

    def generate_bill(self):
        if not self.cart_tree.get_children():
            messagebox.showerror("Error", "Cart is empty")
            return

        customer_name = self.customer_entry.get()
        if not customer_name:
            customer_name = "Walk-in Customer"

        # Calculate total
        total_amount = 0
        bill_items = []
        
        for item in self.cart_tree.get_children():
            item_data = self.cart_tree.item(item, "values")
            item_id = item_data[0]
            quantity = int(item_data[3])
            price = float(item_data[2])
            total_amount += float(item_data[4])
            bill_items.append((item_id, quantity, price))

        # Save bill to database
        bill_id = db.create_bill(customer_name, total_amount, self.current_user["id"], bill_items)

        if not bill_id:
            messagebox.showerror("Error", "Failed to create bill")
            return

        # Generate PDF bill
        self.generate_pdf_bill(bill_id, customer_name, total_amount)

        # Clear cart after successful bill generation
        self.clear_cart()
        self.customer_entry.delete(0, tk.END)

        messagebox.showinfo("Success", f"Bill #{bill_id} generated successfully")

    def generate_pdf_bill(self, bill_id, customer_name, total_amount):
        # Create a temporary file for the PDF
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf_path = temp_file.name
        temp_file.close()

        # Create PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        heading_style = styles["Heading2"]
        normal_style = styles["Normal"]

        # Title
        elements.append(Paragraph("Chai & Grill", title_style))
        elements.append(Paragraph("EXPRESS KITCHEN", heading_style))
        elements.append(Paragraph("We Serve Passion", normal_style))
        elements.append(Spacer(1, 12))

        # Bill details
        elements.append(Paragraph(f"Bill #: {bill_id}", normal_style))
        elements.append(Paragraph(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
        elements.append(Paragraph(f"Customer: {customer_name}", normal_style))
        elements.append(Paragraph(f"Cashier: {self.current_user['username']}", normal_style))
        elements.append(Spacer(1, 12))

        # Get bill items
        bill_items = db.get_bill_items(bill_id)

        # Bill items table
        data = [["Item", "Qty", "Price", "Total"]]
        for item in bill_items:
            data.append([item[0], item[1], f"Rs. {item[2]:.2f}", f"Rs. {item[3]:.2f}"])

        # Add total row
        data.append(["", "", "Grand Total:", f"Rs. {total_amount:.2f}"])

        # Create table
        table = Table(data, colWidths=[250, 70, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -2), 1, colors.black),
            ('BOX', (0, -1), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

        # Footer
        elements.append(Paragraph("Thank you for dining with us!", normal_style))
        elements.append(Paragraph("Please visit again!", normal_style))

        # Build PDF
        doc.build(elements)

        # Open the PDF
        webbrowser.open(pdf_path)

    def show_menu_management(self):
        # Clear main content area
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        # Configure menu management frame
        self.menu_mgmt_frame = tk.Frame(self.dashboard_frame, bg="#000000")
        self.menu_mgmt_frame.pack(fill=tk.BOTH, expand=True)

        # Menu management title
        title_frame = tk.Frame(self.menu_mgmt_frame, bg="#FFC107")
        title_frame.pack(fill=tk.X, pady=10)

        title_label = tk.Label(title_frame, text="Menu Management", font=("Arial", 16, "bold"),
                               bg="#FFC107", fg="#000000", padx=10, pady=5)
        title_label.pack(side=tk.LEFT)

        # Main menu management area
        menu_area = tk.Frame(self.menu_mgmt_frame, bg="#000000")
        menu_area.pack(fill=tk.BOTH, expand=True, pady=10)

        # Split into left and right panels
        left_panel = tk.Frame(menu_area, bg="#000000", width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)

        right_panel = tk.Frame(menu_area, bg="#000000")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Left panel - Categories
        categories_frame = tk.Frame(left_panel, bg="#FFC107")
        categories_frame.pack(fill=tk.BOTH, expand=True)

        categories_label = tk.Label(categories_frame, text="Categories",
                                    font=("Arial", 14, "bold"), bg="#FFC107", fg="#000000", padx=10, pady=5)
        categories_label.pack(fill=tk.X)

        # Categories list
        categories_list_frame = tk.Frame(categories_frame, bg="#FFFFFF")
        categories_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("ID", "Name")
        self.categories_tree = ttk.Treeview(categories_list_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.categories_tree.heading(col, text=col)

        self.categories_tree.column("ID", width=50)
        self.categories_tree.column("Name", width=200)

        self.categories_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.categories_tree.bind("<<TreeviewSelect>>", self.load_category_items)

        # Scrollbar for categories tree
        categories_scrollbar = ttk.Scrollbar(categories_list_frame, orient="vertical",
                                             command=self.categories_tree.yview)
        categories_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.categories_tree.configure(yscrollcommand=categories_scrollbar.set)

        # Category buttons
        category_btn_frame = tk.Frame(categories_frame, bg="#FFC107")
        category_btn_frame.pack(fill=tk.X, padx=10, pady=10)

        add_category_btn = tk.Button(category_btn_frame, text="Add Category", font=("Arial", 12),
                                     bg="#000000", fg="#FFC107", padx=10, pady=5,
                                     command=self.add_category)
        add_category_btn.pack(side=tk.LEFT, padx=5)

        edit_category_btn = tk.Button(category_btn_frame, text="Edit Category", font=("Arial", 12),
                                      bg="#000000", fg="#FFC107", padx=10, pady=5,
                                      command=self.edit_category)
        edit_category_btn.pack(side=tk.LEFT, padx=5)

        delete_category_btn = tk.Button(category_btn_frame, text="Delete Category", font=("Arial", 12),
                                        bg="#000000", fg="#FFC107", padx=10, pady=5,
                                        command=self.delete_category)
        delete_category_btn.pack(side=tk.LEFT, padx=5)

        # Right panel - Menu items
        items_frame = tk.Frame(right_panel, bg="#FFC107")
        items_frame.pack(fill=tk.BOTH, expand=True)

        items_label = tk.Label(items_frame, text="Menu Items",
                               font=("Arial", 14, "bold"), bg="#FFC107", fg="#000000", padx=10, pady=5)
        items_label.pack(fill=tk.X)

        # Menu items list
        items_list_frame = tk.Frame(items_frame, bg="#FFFFFF")
        items_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("ID", "Name", "Price", "Description")
        self.items_tree = ttk.Treeview(items_list_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.items_tree.heading(col, text=col)

        self.items_tree.column("ID", width=50)
        self.items_tree.column("Name", width=150)
        self.items_tree.column("Price", width=80)
        self.items_tree.column("Description", width=200)

        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for items tree
        items_scrollbar = ttk.Scrollbar(items_list_frame, orient="vertical",
                                        command=self.items_tree.yview)
        items_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.items_tree.configure(yscrollcommand=items_scrollbar.set)

        # Item buttons
        item_btn_frame = tk.Frame(items_frame, bg="#FFC107")
        item_btn_frame.pack(fill=tk.X, padx=10, pady=10)

        add_item_btn = tk.Button(item_btn_frame, text="Add Item", font=("Arial", 12),
                                 bg="#000000", fg="#FFC107", padx=10, pady=5,
                                 command=self.add_item)
        add_item_btn.pack(side=tk.LEFT, padx=5)

        edit_item_btn = tk.Button(item_btn_frame, text="Edit Item", font=("Arial", 12),
                                  bg="#000000", fg="#FFC107", padx=10, pady=5,
                                  command=self.edit_item)
        edit_item_btn.pack(side=tk.LEFT, padx=5)

        delete_item_btn = tk.Button(item_btn_frame, text="Delete Item", font=("Arial", 12),
                                    bg="#000000", fg="#FFC107", padx=10, pady=5,
                                    command=self.delete_item)
        delete_item_btn.pack(side=tk.LEFT, padx=5)

        # Load categories and items
        self.load_categories()

    def load_categories(self):
        # Clear existing categories
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)

        # Get categories from database
        categories = db.get_all_categories()

        # Add categories to treeview
        for category in categories:
            self.categories_tree.insert("", "end", values=category)

    def load_category_items(self, event=None):
        selected_category = self.categories_tree.selection()

        if not selected_category:
            # Clear existing items
            for item in self.items_tree.get_children():
                self.items_tree.delete(item)
            return

        category_id = self.categories_tree.item(selected_category, "values")[0]

        # Clear existing items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)

        # Get menu items for selected category
        menu_items = db.get_menu_items_by_category_id(category_id)

        # Add items to treeview
        for item in menu_items:
            self.items_tree.insert("", "end", values=item)

    def add_category(self):
        # Ask for category name
        category_name = simpledialog.askstring("Add Category", "Enter category name:")

        if not category_name:
            return

        # Save category to database
        success = db.add_category(category_name)

        if success:
            messagebox.showinfo("Success", "Category added successfully")
            self.load_categories()
        else:
            messagebox.showerror("Error", "Category already exists")

    def edit_category(self):
        selected_category = self.categories_tree.selection()

        if not selected_category:
            messagebox.showerror("Error", "Please select a category to edit")
            return

        category_id = self.categories_tree.item(selected_category, "values")[0]
        old_category_name = self.categories_tree.item(selected_category, "values")[1]

        # Ask for new category name
        new_category_name = simpledialog.askstring("Edit Category", "Enter new category name:",
                                                   initialvalue=old_category_name)

        if not new_category_name:
            return

        # Update category in database
        success = db.update_category(category_id, new_category_name)

        if success:
            messagebox.showinfo("Success", "Category updated successfully")
            self.load_categories()
        else:
            messagebox.showerror("Error", "Category already exists")

    def delete_category(self):
        selected_category = self.categories_tree.selection()

        if not selected_category:
            messagebox.showerror("Error", "Please select a category to delete")
            return

        category_id = self.categories_tree.item(selected_category, "values")[0]
        category_name = self.categories_tree.item(selected_category, "values")[1]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {category_name}?")

        if not confirm:
            return

        # Delete category from database
        success = db.delete_category(category_id)

        if success:
            messagebox.showinfo("Success", "Category deleted successfully")
            self.load_categories()
        else:
            messagebox.showerror("Error", "Cannot delete category. It is being used by menu items.")

    def add_item(self):
        # Get selected category
        selected_category = self.categories_tree.selection()

        if not selected_category:
            messagebox.showerror("Error", "Please select a category first")
            return

        category_id = self.categories_tree.item(selected_category, "values")[0]

        # Ask for item details
        item_name = simpledialog.askstring("Add Item", "Enter item name:")
        if not item_name:
            return

        item_price = simpledialog.askfloat("Add Item", "Enter item price:")
        if not item_price:
            return

        item_description = simpledialog.askstring("Add Item", "Enter item description:")

        # Save item to database
        success = db.add_menu_item(category_id, item_name, item_price, item_description)

        if success:
            messagebox.showinfo("Success", "Item added successfully")
            self.load_category_items()
        else:
            messagebox.showerror("Error", "Failed to add item")

    def edit_item(self):
        selected_item = self.items_tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select an item to edit")
            return

        item_id = self.items_tree.item(selected_item, "values")[0]
        old_item_name = self.items_tree.item(selected_item, "values")[1]
        old_item_price = self.items_tree.item(selected_item, "values")[2]
        old_item_description = self.items_tree.item(selected_item, "values")[3]

        # Ask for new item details
        new_item_name = simpledialog.askstring("Edit Item", "Enter new item name:",
                                               initialvalue=old_item_name)
        if new_item_name is None:
            return

        new_item_price = simpledialog.askfloat("Edit Item", "Enter new item price:",
                                               initialvalue=old_item_price)
        if new_item_price is None:
            return

        new_item_description = simpledialog.askstring("Edit Item", "Enter new item description:",
                                                      initialvalue=old_item_description)

        # Update item in database
        success = db.update_menu_item(item_id, new_item_name, new_item_price, new_item_description)

        if success:
            messagebox.showinfo("Success", "Item updated successfully")
            self.load_category_items()
        else:
            messagebox.showerror("Error", "Failed to update item")

    def delete_item(self):
        selected_item = self.items_tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select an item to delete")
            return

        item_id = self.items_tree.item(selected_item, "values")[0]
        item_name = self.items_tree.item(selected_item, "values")[1]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {item_name}?")

        if not confirm:
            return

        # Delete item from database
        success = db.delete_menu_item(item_id)

        if success:
            messagebox.showinfo("Success", "Item deleted successfully")
            self.load_category_items()
        else:
            messagebox.showerror("Error", "Cannot delete item. It is being used by bills.")

    def show_user_management(self):
        # Clear main content area
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        # Configure user management frame
        self.user_mgmt_frame = tk.Frame(self.dashboard_frame, bg="#000000")
        self.user_mgmt_frame.pack(fill=tk.BOTH, expand=True)

        # User management title
        title_frame = tk.Frame(self.user_mgmt_frame, bg="#FFC107")
        title_frame.pack(fill=tk.X, pady=10)

        title_label = tk.Label(title_frame, text="User Management", font=("Arial", 16, "bold"),
                               bg="#FFC107", fg="#000000", padx=10, pady=5)
        title_label.pack(side=tk.LEFT)

        # Main user management area
        user_area = tk.Frame(self.user_mgmt_frame, bg="#000000")
        user_area.pack(fill=tk.BOTH, expand=True, pady=10)

        # User list
        user_list_frame = tk.Frame(user_area, bg="#FFFFFF")
        user_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("ID", "Username", "Role")
        self.users_tree = ttk.Treeview(user_list_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.users_tree.heading(col, text=col)

        self.users_tree.column("ID", width=50)
        self.users_tree.column("Username", width=150)
        self.users_tree.column("Role", width=100)

        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for users tree
        users_scrollbar = ttk.Scrollbar(user_list_frame, orient="vertical", command=self.users_tree.yview)
        users_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.users_tree.configure(yscrollcommand=users_scrollbar.set)

        # User buttons
        user_btn_frame = tk.Frame(user_area, bg="#FFC107")
        user_btn_frame.pack(fill=tk.X, padx=10, pady=10)

        add_user_btn = tk.Button(user_btn_frame, text="Add User", font=("Arial", 12),
                                 bg="#000000", fg="#FFC107", padx=10, pady=5,
                                 command=self.add_user)
        add_user_btn.pack(side=tk.LEFT, padx=5)

        edit_user_btn = tk.Button(user_btn_frame, text="Edit User", font=("Arial", 12),
                                  bg="#000000", fg="#FFC107", padx=10, pady=5,
                                  command=self.edit_user)
        edit_user_btn.pack(side=tk.LEFT, padx=5)

        delete_user_btn = tk.Button(user_btn_frame, text="Delete User", font=("Arial", 12),
                                    bg="#000000", fg="#FFC107", padx=10, pady=5,
                                    command=self.delete_user)
        delete_user_btn.pack(side=tk.LEFT, padx=5)

        # Load users
        self.load_users()

    def load_users(self):
        # Clear existing users
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)

        # Get users from database
        users = db.get_all_users()

        # Add users to treeview
        for user in users:
            self.users_tree.insert("", "end", values=user)

    def add_user(self):
        # Ask for user details
        username = simpledialog.askstring("Add User", "Enter username:")
        if not username:
            return

        password = simpledialog.askstring("Add User", "Enter password:", show="*")
        if not password:
            return

        roles = ["admin", "cashier"]
        role = simpledialog.askstring("Add User", "Enter role (admin/cashier):", initialvalue="cashier")
        if role not in roles:
            messagebox.showerror("Error", "Invalid role. Must be admin or cashier.")
            return

        # Save user to database
        success = db.add_user(username, password, role)

        if success:
            messagebox.showinfo("Success", "User added successfully")
            self.load_users()
        else:
            messagebox.showerror("Error", "Username already exists")

    def edit_user(self):
        selected_user = self.users_tree.selection()

        if not selected_user:
            messagebox.showerror("Error", "Please select a user to edit")
            return

        user_id = self.users_tree.item(selected_user, "values")[0]
        old_username = self.users_tree.item(selected_user, "values")[1]
        old_role = self.users_tree.item(selected_user, "values")[2]

        # Ask for new user details
        new_username = simpledialog.askstring("Edit User", "Enter new username:",
                                              initialvalue=old_username)
        if new_username is None:
            return

        new_password = simpledialog.askstring("Edit User", "Enter new password (leave blank to keep old):", show="*")

        roles = ["admin", "cashier"]
        new_role = simpledialog.askstring("Edit User", "Enter new role (admin/cashier):", initialvalue=old_role)
        if new_role not in roles:
            messagebox.showerror("Error", "Invalid role. Must be admin or cashier.")
            return

        # Update user in database
        success = db.update_user(user_id, new_username, new_password, new_role)

        if success:
            messagebox.showinfo("Success", "User updated successfully")
            self.load_users()
        else:
            messagebox.showerror("Error", "Username already exists")

    def delete_user(self):
        selected_user = self.users_tree.selection()

        if not selected_user:
            messagebox.showerror("Error", "Please select a user to delete")
            return

        user_id = self.users_tree.item(selected_user, "values")[0]
        username = self.users_tree.item(selected_user, "values")[1]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {username}?")

        if not confirm:
            return

        # Delete user from database
        success = db.delete_user(user_id)

        if success:
            messagebox.showinfo("Success", "User deleted successfully")
            self.load_users()
        else:
            messagebox.showerror("Error", "Cannot delete user. They may have bills associated with them.")


if __name__ == "__main__":
    # Create the logo file if it doesn't exist
    if not os.path.exists("logo.png"):
        # Create a simple logo
        from PIL import Image, ImageDraw, ImageFont

        img = Image.new('RGBA', (200, 200), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw background
        draw.rectangle([(0, 0), (200, 200)], fill=(255, 193, 7))

        # Draw text
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            font = ImageFont.load_default()

        draw.text((40, 80), "Chai &", fill=(0, 0, 0), font=font)
        draw.text((60, 120), "Grill", fill=(0, 0, 0), font=font)

        img.save("logo.png")

    root = tk.Tk()
    app = ChaiAndGrillApp(root)
    root.mainloop()