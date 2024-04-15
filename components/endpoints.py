from flask_socketio import emit, disconnect
from services.logger import logger

from services.pdf import PDFService
from services.gemini import GeminiService

'''
gemini_service = GeminiService()
pdf_service = PDFService(upload_method=gemini_service.upload_file)
'''

def init_app(app, socketio):
    @socketio.on('connect')
    def handle_connect():
        logger.info("Client connected")
        emit('connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        logger.info("Client disconnected")
        emit('disconnected')
        disconnect()

    @socketio.on('upload_pdf')
    def handle_upload_pdf(data):
        session_id = data['session_id']
        logger.info(f"Received PDF upload for session: {session_id}")
        emit('pdf_received')

        # Save PDF to temp/ folder and name it session_id.pdf
        # content = pdf_service.parse_pdf(f'{session_id}.pdf', session_id)
        # emit('pdf_processed')
        # response = gemini_service.generate_content(content)
        # emit('report_generated')
        # pdf_service.create_pdf_and_json_from_markdown(response, session_id)
        # emit('report_created')

    @socketio.on('request_pdf')
    def handle_request_pdf(data):
        session_id = data['session_id']
        logger.info(f"Request to download PDF for session: {session_id}")
        emit('pdf_requested')

        # file_name = f'{session_id}_report.pdf'
        # pdf_data = pdf_service.get_file(file_name)
        # emit('pdf_data', {'data': pdf_data, 'filename': file_name}, broadcast=False)
        # emit('pdf_sent')

    @socketio.on('request_markdown')
    def handle_request_markdown(data):
        session_id = data['session_id']
        logger.info(f"Request to download Markdown JSON for session: {session_id}")
        emit('markdown_requested')

        # file_name = f"{session_id}_markdown.json"
        # markdown_data = pdf_service.get_file(file_name)
        # emit('pdf_data', {'data': markdown_data, 'filename': file_name}, broadcast=False)
        # emit('markdown_sent')
