import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    'dbname': 'agua_intake',
    'user': 'admin',
    'password': 'admin123',
    'host': 'postgres',
    'port': '5432'
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    insert_query = sql.SQL("""
        INSERT INTO consultas (idade_grupo, peso, total)
        VALUES (%s, %s, %s)
    """)
    cursor.execute(insert_query, ('adulto', 70, 2450))
    conn.commit()
    print("Dados inseridos com sucesso!")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Erro ao conectar com o banco de dados: {e}")