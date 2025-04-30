import mysql.connector

def conectar():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            port=3307,  # sem parênteses e minúsculo
            user='root',  # adicionado parâmetro de usuário
            password='root',
            database='matheuseduardodb_sa'
        )
        print("✅ Conexão estabelecida com sucesso!")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Erro de conexão: {err}")
        return None
    
# pip install mysql-connector-python
