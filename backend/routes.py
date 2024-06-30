from flask import Blueprint, request, jsonify
from prometheus_client import Counter, generate_latest, REGISTRY, Histogram, Gauge
import time
import logging

main = Blueprint("main", __name__)

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

# Exemplo de métrica de contador
requests_total = Counter('requests_total', 'Total de requisições recebidas pelo endpoint', ['endpoint'])

# Exemplo de métrica de histograma para latência
request_latency = Histogram('request_latency_seconds', 'Latência das requisições em segundos', ['endpoint'])

# Exemplo de métrica de gauge para saturação (número de requisições em andamento)
in_progress_requests = Gauge('in_progress_requests', 'Número de requisições em andamento', ['endpoint'])

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
        
        if not peso:
            return jsonify({'error': 'Peso é obrigatório'}), 400
        elif peso < 0:
            return jsonify({'error': 'Peso deve ser maior que 0'}), 400

        if idade_grupo == 'adulto':
            total = peso * 35  # 35 ml por kg para adultos
        elif idade_grupo == 'crianca':
            total = peso * 50  # 50 ml por kg para crianças
        else:
            return jsonify({'error': 'Grupo de Idade Inválido'}), 400

        response = jsonify({'total': total})
        request_latency.labels('/calcular').observe(time.time() - start_time)
        logging.debug(f"Observation in /calcular: {time.time() - start_time}")
        return response
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
