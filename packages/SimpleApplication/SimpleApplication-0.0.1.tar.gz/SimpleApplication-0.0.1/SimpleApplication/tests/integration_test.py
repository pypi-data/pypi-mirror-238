from SimpleApplication.app import app

def test_index_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Simple Python App" in response.data
    assert b"Message from the back-end: Troppo Pacchio!" in response.data
