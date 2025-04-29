from db_config import conectar

conn = conectar()
if conn:
    print("✅ Conexão bem-sucedida!")
    conn.close()
else:
    print("❌ Falha na conexão!")