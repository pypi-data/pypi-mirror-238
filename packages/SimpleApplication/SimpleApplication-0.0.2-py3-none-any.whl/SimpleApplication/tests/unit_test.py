from SimpleApplication.app import app

def test_hello_world():
    client = app.test_client()
    response = client.get('/')
    assert b"Welcome to the Simple Python App" in response.data

def test_message_from_backend():
    client = app.test_client()
    response = client.get('/')
    assert b"Message from the back-end: Troppo Pacchio!" in response.data
