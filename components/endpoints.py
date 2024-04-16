from flask_socketio import emit, disconnect
from services.logger import logger
import json

from services.pdf import PDFService
from services.gemini import GeminiService

# Initialize services
gemini_service = GeminiService()
pdf_service = PDFService(upload_method=gemini_service.upload_file)

def init_app(app, socketio):
    @socketio.on('connect')
    def handle_connect():
        logger.info("A client has connected.")
        emit('connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        logger.info("A client has disconnected.")
        disconnect()
        emit('disconnected')

    @socketio.on('upload_pdf')
    def handle_upload_pdf(data):
        session_id = data.get('session_id')
        logger.info(f"Received PDF upload request for session ID: {session_id}")

        # Save the User's PDF to temp/ folder
        pdf_file_path = f'temp/{session_id}.pdf'
        with open(pdf_file_path, 'wb') as pdf_file:
            pdf_file.write(data['pdf_data'])
        logger.info(f"PDF file saved successfully: {pdf_file_path}")

        # Parse the PDF for text and images
        content = pdf_service.parse_pdf(f'{session_id}.pdf', session_id)
        logger.info(f"PDF parsing completed for: {session_id}")

        # Ensure the content is serializable
        serializable_content = []
        for item in content:
            if isinstance(item['data'], bytes):
                item['data'] = item['data'].decode('utf-8')
            serializable_content.append(item)

        # Save content to a JSON file
        json_path = f'temp/{session_id}.json'
        try:
            with open(json_path, 'w') as json_file:
                json.dump(serializable_content, json_file)
            logger.info(f"Content from PDF has been saved to JSON: {json_path}")
        except Exception as e:
            logger.error(f"Failed to save content to JSON at {json_path}: {e}")

        # Generate content from parsed PDF
        response = gemini_service.generate_content(content)
        logger.info(f"Generated content for session: {session_id}")

        # Generate and save PDF/Markdown from response
        pdf_service.create_pdf_and_json_from_markdown(response, session_id)
        logger.info(f"Final report PDF and Markdown created for session: {session_id}")

    @socketio.on('request_pdf')
    def handle_request_pdf(data):
        session_id = data['session_id']
        logger.info(f"Request received to download PDF for session ID: {session_id}")
        file_name = f'{session_id}_report.pdf'
        pdf_data = pdf_service.get_file(file_name)
        emit('pdf_data', {'data': pdf_data, 'filename': file_name}, broadcast=False)


    @socketio.on('request_markdown')
    def handle_request_markdown(data):
        session_id = data['session_id']
        logger.info(f"Request received to download Markdown JSON for session ID: {session_id}")
        emit('markdown_requested')
        file_name = f"{session_id}_markdown.json"
        markdown_data = pdf_service.get_file(file_name)
        emit('pdf_data', {'data': markdown_data, 'filename': file_name}, broadcast=False)

