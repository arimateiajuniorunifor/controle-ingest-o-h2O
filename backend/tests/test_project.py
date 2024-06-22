def test_home(client):
    response = client.get('/')
    assert "Backend está no Ar!" in response.data