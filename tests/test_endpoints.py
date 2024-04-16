import pytest
import socketio
import os
import json

@pytest.fixture(scope="module")
def sio_client():
    sio = socketio.Client(logger=True, engineio_logger=True)
    sio.connect('http://127.0.0.1:5000', namespaces=['/'])
    yield sio
    sio.disconnect()

def test_connect(sio_client):
    assert sio_client.connected

def test_upload_pdf(sio_client):
    # Path to the test PDF file
    pdf_file_path = 'samples/report_with_images.pdf'

    # Read the PDF file as binary
    with open(pdf_file_path, 'rb') as file:
        pdf_data = file.read()

    # Emit the upload_pdf event with session_id and pdf_data
    sio_client.emit('upload_pdf', {'session_id': '123', 'pdf_data': pdf_data})
    assert 'pdf_received'


def test_request_pdf(sio_client):
    download_path = './samples/test_downloads/'
    
    def handle_file_data(data):
        # Use the helper function to save the file
        file_path = save_file(data, download_path)
        print(f"PDF saved to {file_path}")

    sio_client.on('pdf_data', handler=handle_file_data, namespace='/')
    sio_client.emit('request_pdf', {'session_id': '123'}, namespace='/')
    sio_client.sleep(1)  # Wait for the event to be handled

def test_request_markdown(sio_client):
    download_path = './samples/test_downloads/'
    
    def handle_file_data(data):
        # Use the same helper function to save the file
        file_path = save_file(data, download_path)
        print(f"Markdown JSON saved to {file_path}")

    sio_client.on('pdf_data', handler=handle_file_data, namespace='/')
    sio_client.emit('request_markdown', {'session_id': '123'}, namespace='/')
    sio_client.sleep(1)  # Wait for the event to be handled


def test_disconnect(sio_client):
    sio_client.disconnect()
    assert not sio_client.connected



def save_file(data, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    file_path = os.path.join(download_path, data['filename'])
    
    # Determine how to save the file based on its content type
    if file_path.endswith('.pdf'):
        # Ensure data is in bytes before writing to a binary file
        with open(file_path, 'wb') as file:
            if isinstance(data['data'], list):
                # Convert list to bytes if necessary, this part might need specific handling
                file.write(bytes(data['data']))
            else:
                file.write(data['data'])
    else:
        # Assuming JSON or text data can be directly serialized or written
        with open(file_path, 'w') as file:
            if isinstance(data['data'], (dict, list)):
                # Convert dictionary or list to JSON string
                json.dump(data['data'], file)
            else:
                file.write(str(data['data']))

    assert os.path.exists(file_path), f"File not saved: {file_path}"
    return file_path