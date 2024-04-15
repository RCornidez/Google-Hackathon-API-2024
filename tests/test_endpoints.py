import pytest
import socketio

@pytest.fixture(scope="module")
def sio_client():
    sio = socketio.Client(logger=True, engineio_logger=True)
    sio.connect('http://127.0.0.1:5000', namespaces=['/'])
    yield sio
    sio.disconnect()

def test_connect(sio_client):
    assert sio_client.connected

def test_upload_pdf(sio_client):
    sio_client.emit('upload_pdf', {'session_id': '123'})
    assert 'pdf_received'

def test_request_pdf(sio_client):
    sio_client.emit('request_pdf', {'session_id': '123'})
    assert 'pdf_requested'

def test_request_markdown(sio_client):
    sio_client.emit('request_markdown', {'session_id': '123'})
    assert 'markdown_requested'

def test_disconnect(sio_client):
    sio_client.disconnect()
    assert not sio_client.connected
