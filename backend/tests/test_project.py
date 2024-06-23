def test_home(client):
    response = client.get('/')
    assert b"Backend online!" in response.data