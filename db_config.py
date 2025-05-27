import mysql.connector

def conectar():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3307,
            user='root',  
            password='root',
            database='matheuseduardodb_sa'
        )
        print("✅ Conexão estabelecida com sucesso!")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Erro de conexão: {err}")
        return None
    
# pip install mysql-connector-python