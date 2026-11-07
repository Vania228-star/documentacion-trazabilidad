from app import app

def test_hello():
    client = app.test_client()
    response = client.get('/hello?name=Vania')
    assert response.status_code == 200
    assert b"Hello, Vania!" in response.data