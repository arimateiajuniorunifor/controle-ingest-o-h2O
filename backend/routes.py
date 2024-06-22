from flask import Blueprint, request, jsonify
from prometheus_client import Counter, generate_latest, REGISTRY

main = Blueprint("main", __name__)

# Exemplo de métrica de contador
requests_total = Counter('requests_total', 'Total de requisições recebidas pelo endpoint', ['endpoint'])

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

    return jsonify({'total': total})