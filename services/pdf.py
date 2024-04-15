import fitz  # PyMuPDF
import io
import pypandoc
import os
import json
from services.logger import logger

class PDFService:
    def __init__(self, upload_method):
        self.upload = upload_method

    def parse_pdf(self, pdf_path, session_id):
        pdf = fitz.open(pdf_path)
        content = []
        image_count = 0  # Initialize image counter
        logger.info(f"Starting to parse PDF: {pdf_path}")

        for page_num, page in enumerate(pdf, start=1):
            blocks = page.get_text("dict")["blocks"]
            blocks.sort(key=lambda b: (b["bbox"][1], b["bbox"][0]))  # Sort by y-coordinate then x

            for block in blocks:
                if block['type'] == 0:  # Text block
                    text = " ".join([line['text'] for line in block['lines']])
                    content.append({'type': 'text', 'data': text, 'page': page_num, 'position': block['bbox']})
                elif block['type'] == 1:  # Image block
                    xref = block['image']
                    base_image = pdf.extract_image(xref)
                    if base_image:
                        image_bytes = base_image["image"]
                        img = io.BytesIO(image_bytes)
                        img_name = f"{session_id}_image{image_count}.jpg"
                        image_url = self.upload(img, img_name)
                        content.append({'type': 'image', 'data': image_url, 'page': page_num, 'position': block['bbox']})
                        image_count += 1

        logger.info(f"Finished parsing PDF: {pdf_path}")
        return content

    def create_pdf_and_json_from_markdown(self, markdown_text, session_id):
        output_dir = '/temp'
        os.makedirs(output_dir, exist_ok=True)
        json_filename = os.path.join(output_dir, f"{session_id}_markdown.json")
        pdf_filename = os.path.join(output_dir, f"{session_id}_report.pdf")

        with open(json_filename, 'w') as json_file:
            json.dump({'markdown': markdown_text}, json_file, indent=4)
            logger.info(f"Markdown saved to JSON file: {json_filename}")

        output = pypandoc.convert_text(markdown_text, 'pdf', format='md', outputfile=pdf_filename)
        logger.info(f"PDF generated at: {pdf_filename}")

        return json_filename, pdf_filename

    def get_file(self, file_name):
        file_directory = '/temp'
        file_path = os.path.join(file_directory, file_name)

        if not os.path.exists(file_path):
            logger.error(f"File {file_name} not found")
            return None, "File not found"

        try:
            with open(file_path, 'rb') as pdf_file:
                pdf_data = pdf_file.read()
            return pdf_data, None
        except IOError as error:
            logger.error(f"Failed to read file {file_name}: {error}")
            return None, str(error)
