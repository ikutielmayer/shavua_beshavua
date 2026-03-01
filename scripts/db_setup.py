import mysql.connector
from mysql.connector import errorcode

db_config = {
    'user': 'ikutiel',
    'password': 'B7654321b',
    'host': 'localhost',
    'port': 3306
}

def create_database():
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS shavua_beshavua DEFAULT CHARACTER SET 'utf8mb4'")
        print("Database 'shavua_beshavua' created or already exists.")
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

if __name__ == "__main__":
    create_database()
