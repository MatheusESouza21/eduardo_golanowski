MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'matheuseduardodb_sa'
import mysql.connector

def conectar():
 
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='matheuseduardodb_sa'
    )
# pip install mysql-connector-python