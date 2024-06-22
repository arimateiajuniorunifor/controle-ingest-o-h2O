import json


class TestCalcular:
    def test_adulto_80kg(self, client):
        idade_grupo = "adulto"
        peso = 80

        payload = {
            "idade_grupo": idade_grupo,
            "peso": peso
        }

        response = client.post("/calcular", content_type='application/json', data=json.dumps(payload))

        response_json = response.get_json()

        calc_result = 35 * 80  # 2800

        assert response_json['total'] == calc_result
        assert response.status_code == 200
    
    def test_crianca_32_5kg(self, client):
        idade_grupo = "crianca"
        peso = 32.5

        payload = {
            "idade_grupo": idade_grupo,
            "peso": peso
        }

        response = client.post("/calcular", content_type='application/json', data=json.dumps(payload))

        response_json = response.get_json()

        calc_result = 50 * 32.5  # 1625

        assert response_json['total'] == calc_result
        assert response.status_code == 200
    
    def test_error_0kg(self, client):
        idade_grupo = "crianca"
        peso = 0

        payload = {
            "idade_grupo": idade_grupo,
            "peso": peso
        }

        response = client.post("/calcular", content_type='application/json', data=json.dumps(payload))

        response_json = response.get_json()

        assert response_json.get("error", None) == "Peso é obrigatório"
        assert response.status_code == 400


    def test_error_peso_negativo(self, client):
        idade_grupo = "adulto"
        peso = -20

        payload = {
            "idade_grupo": idade_grupo,
            "peso": peso
        }

        response = client.post("/calcular", content_type='application/json', data=json.dumps(payload))

        response_json = response.get_json()

        assert response_json.get("error", None) == "Peso deve ser maior que 0"
        assert response.status_code == 400
    
    def test_error_no_idade_grupo(self, client):
        peso = 100

        payload = {
            "peso": peso
        }

        response = client.post("/calcular", content_type='application/json', data=json.dumps(payload))

        response_json = response.get_json()

        assert response_json.get("error", None) == "Grupo de Idade Inválido"
        assert response.status_code == 400

    def test_error_no_peso(self, client):
        idade_grupo = "crianca"

        payload = {
            "idade_grupo": idade_grupo,
        }

        response = client.post("/calcular", content_type='application/json', data=json.dumps(payload))

        response_json = response.get_json()

        assert response_json.get("error", None) == "Peso é obrigatório"
        assert response.status_code == 400
