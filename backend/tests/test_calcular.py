import json

def test_calcular(client):
    test_cases = [
        {
            "idade_grupo": "adulto",
            "peso": 80
        },
        # TODO: ver como vai ser feito no caso de erro
        {
            "idade_grupo": "adulto",
            "peso": -1
        },
    ]
    for payload in test_cases:
        response = client.post("/calcular", data=payload)

        response_json = json.load(response.data)

        ml_agua = 0

        if payload["idade_grupo"] == "adulto":
            ml_agua = 35
        elif payload["idade_grupo"] == "crianca":
            ml_agua = 50

        assert response_json['total'] == payload["peso"] * ml_agua