# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from prometheus_client import Counter, generate_latest, REGISTRY

# app = Flask(__name__)
# CORS(app)

# # Exemplo de métrica de contador
# requests_total = Counter('requests_total', 'Total de requisições recebidas pelo endpoint', ['endpoint'])

# @app.route('/', methods=['GET'])
# def home():
#     return "Backend está no Ar!", 200

# @app.route('/metrics')
# def metrics():
#     # Registro de métrica de contador
#     requests_total.labels('/metrics').inc()

#     # Retorna as métricas no formato Prometheus
#     return generate_latest(REGISTRY), 200

# @app.route('/calcular', methods=['POST'])
# def calcular():
#     data = request.json
#     idade_grupo = data.get('idade_grupo')
#     peso = data.get('peso')
    
#     if not peso:
#         return jsonify({'error': 'Peso é obrigatório'}), 400

#     if idade_grupo == 'adulto':
#         total = peso * 35  # 35 ml por kg para adultos
#     elif idade_grupo == 'crianca':
#         total = peso * 50  # 50 ml por kg para crianças
#     else:
#         return jsonify({'error': 'Grupo de Idade Inválido'}), 400

#     return jsonify({'total': total})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)