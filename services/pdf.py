import fitz  # PyMuPDF
import io
import os
import json
from services.logger import logger
import markdown2
from weasyprint import HTML
import base64
from flask import Flask, jsonify, send_file

class PDFService:
    def __init__(self, upload_method):
        self.upload = upload_method
        logger.info("PDF Service initialized.")

    def parse_pdf(self, pdf_file, session_id):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        pdf_path = os.path.join(base_dir, "temp", pdf_file)
        pdf = fitz.open(pdf_path)
        content = []
        image_count = 0
        logger.info(f"Starting PDF parse for: {pdf_path}")

        for page_num, page in enumerate(pdf, start=1):
            text = page.get_text("text")
            if text:
                content.append({'type': 'text', 'data': text, 'page': page_num})

            for img_info in page.get_images(full=True):
                xref = img_info[0]
                base_image = pdf.extract_image(xref)
                if base_image:
                    image_bytes = base_image["image"]
                    img = io.BytesIO(image_bytes)
                    img_name = f"{session_id}_{image_count}.jpg"
                    temp_image_path = os.path.join(base_dir, "temp", img_name)
                    
                    with open(temp_image_path, 'wb') as f:
                        f.write(img.getbuffer())
                    
                    try:
                        image_url = self.upload(img_name, session_id)
                        content.append({'type': 'image', 'data': image_url, 'position': img_info[2], 'page': page_num})
                        logger.info(f"Uploaded image {img_name} to URL: {image_url}")
                        image_count += 1
                    except Exception as e:
                        logger.error(f"Failed to upload image {img_name}: {e}")

        logger.info(f"Completed parsing PDF: {pdf_path}")
        return content

    def create_pdf_and_json_from_markdown(self, markdown_text, session_id):
        output_dir = 'temp/'
        os.makedirs(output_dir, exist_ok=True)

        json_filename = os.path.join(output_dir, f"{session_id}_markdown.json")
        markdown_filename = os.path.join(output_dir, f"{session_id}_markdown.md")
        pdf_filename = os.path.join(output_dir, f"{session_id}_report.pdf")

        with open(json_filename, 'w') as json_file:
            json.dump({'markdown': markdown_text}, json_file, indent=4)
            logger.info(f"Markdown content saved to JSON: {json_filename}")

        with open(markdown_filename, 'w') as md_file:
            md_file.write(markdown_text)
            logger.info(f"Markdown content saved to file: {markdown_filename}")

        self.markdown_to_pdf(markdown_text, pdf_filename)
        logger.info(f"Generated PDF: {pdf_filename}")

    def markdown_to_pdf(self, markdown_text, pdf_file):
        html_content = markdown2.markdown(markdown_text)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(base_dir, '..', 'components', 'templates', 'template.html')
        css_path = os.path.join(base_dir, '..', 'components', 'templates', 'style.css')

        with open(template_path, 'r') as file:
            template = file.read()
        rendered_html = template.replace('{{ content }}', html_content)

        HTML(string=rendered_html, base_url=os.path.dirname(template_path)).write_pdf(pdf_file, stylesheets=[css_path])
        logger.info(f"PDF creation successful for: {pdf_file}")

    def get_pdf_file(self, file_name):
        file_directory = 'temp'
        file_path = os.path.join(file_directory, file_name)

        if not os.path.exists(file_path):
            logger.error(f"File {file_name} not found")
            return "File not found"

        try:
            with open(file_path, 'rb') as pdf_file:
                pdf_data = pdf_file.read()
                pdf_data_base64 = base64.b64encode(pdf_data).decode('utf-8')  # Convert to base64 string
            return pdf_data_base64
        except IOError as error:
            logger.error(f"Failed to read file {file_name}: {error}")
            return str(error)

    def get_markdown_file(self, file_name):
        file_directory = 'temp'
        file_path = os.path.join(file_directory, file_name)

        if not os.path.exists(file_path):
            logger.error(f"File {file_name} not found")
            return None, "File not found"

        try:
            with open(file_path, 'r') as markdown_file:
                markdown_data = json.load(markdown_file)

            return markdown_data
        except IOError as error:
            logger.error(f"Failed to read file {file_name}: {error}")
            return None, str(error)
