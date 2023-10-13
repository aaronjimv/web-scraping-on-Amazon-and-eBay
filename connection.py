import mysql.connector as mysql

def connect():
    '''
    Establishes a connection to the MySQL database.

    Returns:
        mysql.connector.connection_cext.CMySQLConnection: A MySQL connection object if successful.
        If an error occurs during connection, prints an error message and returns None.
    '''
    try:
        connection = mysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'web_scraping'
        )
        print("Conectado a la base de datos")
        return connection
    except mysql.Error as err:
        print("ERROR: "+err)