import connection


class Products:
    def __init__(self, name, amazon_url, ebay_url, amazon_price, ebay_price):
        '''
        Initializes a Products object with the provided attributes.

        Parameters:
            name (str): The name of the product.
            amazon_url (str): The URL of the product on Amazon.
            ebay_url (str): The URL of the product on eBay.
            amazon_price (float): The price of the product on Amazon.
            ebay_price (float): The price of the product on eBay.
        '''
        self.name = name
        self.amazon_url = amazon_url
        self.ebay_url = ebay_url
        self.amazon_price = amazon_price
        self.ebay_price = ebay_price

    def save_products(self):
        '''
        Saves the product information into the database.

        Returns:
            str: A message indicating whether the operation
            was successful or an error occurred.
        '''
        try:
            conn = connection.connect()
            cursor = conn.cursor()
            sql = """insert into products(
                        name,
                        amazon_url,
                        ebay_url,
                        amazon_price,
                        ebay_price
            ) values (%s, %s, %s, %s, %s)"""
            datos = (
                self.name,
                self.amazon_url,
                self.ebay_url,
                self.amazon_price,
                self.ebay_price
            )
            cursor.execute(sql, datos)
            conn.commit()
            conn.close()
            return "\nSaved Products\n"
        except connection.Error as err:
            return "ERROR"+err

    def get_products(self):
        '''
        Retrieves all products from the database.

        Returns:
            list: A list of tuples representing product information
            (name, amazon_url, ebay_url, amazon_price, ebay_price).

            If an error occurs, returns an error message.
        '''
        try:
            conn = connection.connect()
            cursor = conn.cursor()
            sql = 'select * from products'
            cursor.execute(sql)
            products = cursor.fetchall()
            conn.close()
            return products
        except connection.Error as err:
            return "ERROR"+err
