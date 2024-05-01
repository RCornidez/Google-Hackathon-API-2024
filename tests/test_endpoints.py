import pytest
import socketio
import os
import json
import time
import base64
from pathlib import Path

@pytest.fixture(scope="module")
def sio_client():
    sio = socketio.Client(logger=True, engineio_logger=True)
    sio.connect('http://127.0.0.1:5000')
    yield sio
    sio.disconnect()

def test_connect(sio_client):
    assert sio_client.connected, "Client failed to connect"

def test_upload_pdf(sio_client):
    pdf_file_path = 'samples/report_with_images.pdf'
    with open(pdf_file_path, 'rb') as file:
        pdf_data = file.read()
    file_parsed_received = []
    sio_client.on('file_parsed', lambda: file_parsed_received.append(True))
    sio_client.emit('upload_pdf', {'session_id': '123', 'pdf_data': pdf_data})
    time.sleep(5)
    assert file_parsed_received, "File parsed event not received; PDF may not have been processed successfully."

def test_request_pdf(sio_client):
    download_path = './samples/test_downloads/'
    os.makedirs(download_path, exist_ok=True)
    received_files = []
    def handle_pdf_data(data):
        base64_string = data['data']
        file_name = data.get('filename', 'downloaded_report.pdf')
        file_path = os.path.join(download_path, file_name)
        pdf_bytes = base64.b64decode(base64_string)
        with open(file_path, 'wb') as file:
            file.write(pdf_bytes)
        assert os.path.exists(file_path), f"PDF not saved: {file_path}"
        received_files.append(file_path)
    sio_client.on('pdf_data', handle_pdf_data)
    sio_client.emit('request_pdf', {'session_id': '123'})
    time.sleep(2)
    assert received_files, "No PDF file was received."

def test_request_markdown(sio_client):
    download_path = './samples/test_downloads/'
    os.makedirs(download_path, exist_ok=True)
    received_files = []

    def handle_markdown_data(data):
        file_name = data.get('filename', 'downloaded_markdown.json')
        file_path = os.path.join(download_path, file_name)
        with open(file_path, 'w') as file:
            json.dump(data['data'], file)
        assert os.path.exists(file_path), f"Markdown JSON not saved: {file_path}"
        received_files.append(file_path)
        print(f"Markdown JSON saved to {file_path}")

    sio_client.on('markdown_data', handle_markdown_data)
    sio_client.emit('request_markdown', {'session_id': '123'})
    time.sleep(2)  # Allow some time for the event and file save operation
    assert received_files, "No Markdown file was received."

def save_file(data, download_path):
    file_path = Path(download_path) / data['filename']
    mode = 'wb' if file_path.suffix == '.pdf' else 'w'
    with open(file_path, mode) as file:
        if isinstance(data['data'], str):
            file.write(data['data'].encode('utf-8') if mode == 'wb' else data['data'])
        elif isinstance(data['data'], (dict, list)):
            json.dump(data['data'], file)
        else:
            raise ValueError("Unsupported data type")
    return str(file_path)
