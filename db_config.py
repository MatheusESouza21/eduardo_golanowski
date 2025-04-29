import mysql.connector

def conectar():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='matheuseduardodb_sa'
        )
        return conexao
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None
    
# pip install mysql-connector-python