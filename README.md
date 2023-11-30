# Web Scraping and Price Monitor

This project includes scripts for simple web scraping on Amazon and eBay and monitoring product prices. It also stores the data in a MySQL database for tracking.

### `main.py`

This main script allows the user to search for products on Amazon and eBay, compare prices, and record products in a database. It also initiates a thread to monitor prices and display real-time changes.

### `products.py`

This script defines the `Products` class used to interact with the database and perform save and retrieve product data operations.

### `connection.py`

This script establishes a connection with a MySQL database. A XAMPP installation is required to run the database.

## Required Libraries

Ensure you have the following Python libraries installed before running the scripts:

- `selenium` (for web scraping).
- `beautifulsoup4` (for HTML parsing).
- `mysql-connector-python` (for communicating with the MySQL database).
- `threading` (for managing threads).
