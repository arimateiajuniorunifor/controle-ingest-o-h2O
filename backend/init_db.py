import psycopg2
import os

def initialize_db():
    conn = psycopg2.connect(
        dbname="agua_intake",
        user="admin",
        password="admin123",  # Substitua com a senha correta
        host="postgres"            # Nome do serviço do PostgreSQL no Docker Compose
    )
    cursor = conn.cursor()
    with open('/app/init_db.sql', 'r') as f:
        cursor.execute(f.read())
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    initialize_db()
