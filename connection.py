import mysql.connector as mysql

def connect():
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