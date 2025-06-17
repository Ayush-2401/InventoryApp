InventoryApp
A simple Inventory Management Application for stores, built using PySide6 for the Graphical User Interface (GUI) and SQLAlchemy with SQLite for robust data management.

Table of Contents
Features
Getting Started
Prerequisites
Installation and Setup
Running the Application
Usage
Login Screen
Main Menu
Using the Forms
Database
Viewing Database Data
Project Structure
Default Credentials
Features
User Login: Secure login system with predefined credentials for different roles.
Product Master: Allows users to add, view, and manage detailed product information, including barcode, SKU, category, product name, description, tax, price, unit of measurement, and an associated image path.
Goods Receiving: Enables the recording of incoming inventory from suppliers, which automatically updates the stock quantity of corresponding products.
Sales Entry: Facilitates the recording of sales transactions, automatically deducting the sold quantity from product stock.
SQLite Database: All application data is persistently stored in a local inventory.db SQLite database file, ensuring data integrity and availability.
Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
Ensure you have Python 3.8 or newer installed on your system.

You will also need the following Python libraries, which can be installed via pip:

PySide6: For the graphical user interface.
SQLAlchemy: For interacting with the SQLite database.
You can install them using the following command:

Bash

pip install PySide6 SQLAlchemy
Installation and Setup
Clone the Repository:

Bash

git clone https://github.com/YourGitHubUsername/InventoryApp.git
cd InventoryApp
(Remember to replace https://github.com/YourGitHubUsername/InventoryApp.git with the actual URL of your GitHub repository once it's created.)

Delete Existing Database (Crucial for First Run or Fresh Start):
If you have run the application before and there's an inventory.db file in your project directory, delete it. This ensures a clean database is created with all tables and the initial default user data.

Bash

# On Windows
del inventory.db

# On macOS/Linux
rm inventory.db
Running the Application
Once you are in the project directory and have deleted inventory.db (if it existed), run the main application file:

Bash

python app.py
The application's login window should appear.

Usage
Login Screen
Upon launching, you will see a login window. Use one of the predefined credentials to access the application:

Main Menu
After a successful login, the main application window will be displayed. This window provides access to the core modules of the inventory system via three buttons:

Product Master: Click this button to open the form for managing product details.
Goods Receiving: Click this button to open the form for recording incoming inventory.
Sales Entry: Click this button to open the form for recording product sales.
Using the Forms
Product Master Form: Fill in details such as Barcode, SKU ID, Product Name, Category, Subcategory, Description, Tax, Price, and Unit. You can also upload an image for the product. Click "Save Product" to add it to the database.
Goods Receiving Form: Enter the Product ID, Supplier Name, Quantity, Unit, Rate per unit, and Tax. The system will calculate the total cost and update the product's stock quantity.
Sales Entry Form: Enter the Product ID, Customer Name, Quantity, Unit, and Rate per unit. The system will calculate the total sale amount and deduct the quantity from the product's available stock. A warning will be displayed if stock is insufficient.
Database
The application utilizes a local SQLite database named inventory.db. This file is automatically created and managed by SQLAlchemy when you run app.py for the first time (or after deleting an old inventory.db file).

Viewing Database Data
You can easily inspect the data stored in your inventory.db file using a dedicated SQLite database browser.

Download DB Browser for SQLite:
Visit https://sqlitebrowser.org/ and download the appropriate version for your operating system.
Install DB Browser for SQLite:
Follow the installation instructions for your system.
Open inventory.db:
Launch "DB Browser for SQLite".
Click on the "Open Database" button and navigate to your InventoryApp project directory.
Select the inventory.db file and click "Open".
Browse Data:
Go to the "Browse Data" tab. You can then select any table (e.g., operators, products, goods_receiving, sales) from the dropdown menu to view its contents.
Project Structure
The project is organized into modular files for better readability and maintainability:

InventoryApp/
├── app.py                  # Main application entry point and window
├── db_setup.sql            # SQL schema definition (for reference, actual creation via models.py)
├── models.py               # Defines SQLAlchemy ORM models for database tables
├── ui_login.py             # Login form UI and logic
├── ui_product_master.py    # Product Master form UI and logic
├── ui_goods_receiving.py   # Goods Receiving form UI and logic
├── ui_sales.py             # Sales Entry form UI and logic
└── utils.py                # Database engine and session setup utilities
Default Credentials
For initial login, use the following credentials:

Username: admin Password: adminpass
Username: user Password: userpass
