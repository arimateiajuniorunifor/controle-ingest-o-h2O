import os
from flask import Blueprint, request, jsonify
from prometheus_client import Counter, generate_latest, REGISTRY, Histogram, Gauge
import time
import logging
import psycopg2
from psycopg2 import sql

main = Blueprint("main", __name__)

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

# Exemplo de métrica de contador
requests_total = Counter('requests_total', 'Total de requisições recebidas pelo endpoint', ['endpoint'])

# Exemplo de métrica de histograma para latência
request_latency = Histogram('request_latency_seconds', 'Latência das requisições em segundos', ['endpoint'])

# Exemplo de métrica de gauge para saturação (número de requisições em andamento)
in_progress_requests = Gauge('in_progress_requests', 'Número de requisições em andamento', ['endpoint'])

# Configurações do banco de dados
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'agua_intake'),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD', 'admin123'),
    'host': os.getenv('DB_HOST', 'postgres'),  # Alterado para 'postgres' conforme o Docker Compose
    'port': os.getenv('DB_PORT', '5432')
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logging.debug("Conexão com o banco de dados estabelecida com sucesso.")
        return conn
    except Exception as e:
        logging.error(f"Erro ao conectar com o banco de dados: {e}")
        raise

def test_db_connection():
    try:
        conn = get_db_connection()
        conn.close()
        logging.info("Conexão com o banco de dados testada com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao testar a conexão com o banco de dados: {e}")

# Chame test_db_connection() no início do seu script para verificar a conexão
test_db_connection()

@main.route('/', methods=['GET'])
def home():
    return "Backend online!", 200

@main.route('/metrics')
def metrics():
    # Registro de métrica de contador
    requests_total.labels('/metrics').inc()

    # Retorna as métricas no formato Prometheus
    return generate_latest(REGISTRY), 200

@main.route('/calcular', methods=['POST'])
def calcular():
    start_time = time.time()
    in_progress_requests.labels('/calcular').inc()
    logging.debug(f"Increment in /calcular: {in_progress_requests.labels('/calcular')._value.get()}")
    try:
        data = request.json
        idade_grupo = data.get('idade_grupo')
        peso = data.get('peso', 0)
        
        if peso is None:
            return jsonify({'error': 'Peso é obrigatório'}), 400
        elif peso < 0:
            return jsonify({'error': 'Peso deve ser maior que 0'}), 400

        if idade_grupo == 'adulto':
            total = peso * 35  # 35 ml por kg para adultos
        elif idade_grupo == 'crianca':
            total = peso * 50  # 50 ml por kg para crianças
        elif idade_grupo == 'gravida':
            total = peso * 35 + 300  # 35 ml por kg para grávidas, mais 300 ml
        else:
            return jsonify({'error': 'Grupo de Idade Inválido'}), 400

        # Inserir dados no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()
        insert_query = sql.SQL("""
            INSERT INTO consultas (idade_grupo, peso, total)
            VALUES (%s, %s, %s)
        """)
        cursor.execute(insert_query, (idade_grupo, peso, total))
        conn.commit()
        logging.debug("Dados inseridos com sucesso!")
        cursor.close()
        conn.close()

        response = jsonify({'total': total})
        request_latency.labels('/calcular').observe(time.time() - start_time)
        logging.debug(f"Observation in /calcular: {time.time() - start_time}")
        return response
    except Exception as e:
        logging.error(f"Erro ao processar a requisição: {e}")
        return jsonify({'error': 'Erro ao processar a requisição'}), 500
    finally:
        in_progress_requests.labels('/calcular').dec()
        logging.debug(f"Decrement in /calcular: {in_progress_requests.labels('/calcular')._value.get()}")

# Adicionando middleware para medir requisições em andamento
@main.before_request
def before_request():
    in_progress_requests.labels(request.path).inc()
    logging.debug(f"Increment in before_request: {in_progress_requests.labels(request.path)._value.get()}")

@main.after_request
def after_request(response):
    in_progress_requests.labels(request.path).dec()
    logging.debug(f"Decrement in after_request: {in_progress_requests.labels(request.path)._value.get()}")
    return response

@main.teardown_request
def teardown_request(exception):
    in_progress_requests.labels(request.path).dec()
    logging.debug(f"Decrement in teardown_request: {in_progress_requests.labels(request.path)._value.get()}")
    return None
