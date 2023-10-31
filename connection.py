import mysql.connector as mysql


def connect():
    '''
    Establishes a connection to the MySQL database.

    Returns:
        mysql.connector.connection_cext.CMySQLConnection:
        A MySQL connection object if successful.

        If an error occurs during connection, prints an
        error message and returns None.
    '''
    try:
        connection = mysql.connect(
            host='localhost',
            port=33065,
            user='root',
            password='',
            database='web_scraping'
        )
        print("\n- Connected to the database -")
        return connection
    except mysql.Error as err:
        print(f'ERROR:\n {err}\n')
