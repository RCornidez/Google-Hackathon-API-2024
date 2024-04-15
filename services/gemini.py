import google.generativeai as genai
import os
from dotenv import load_dotenv
from services.logger import logger

class GeminiService:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")

        # Initialize Google API Client
        genai.configure(api_key=api_key)
        logger.info("Google Generative AI API client configured.")

    def upload_file(self, file_name, display_name):
        """Upload a file to the GenAI File API."""
        try:
            file_path = "/temp/" + file_name
            response = genai.upload_file(path=file_path, display_name=display_name)
            logger.info(f"Uploaded file {response.display_name} as: {response.uri}")
            return response.uri
        except Exception as e:
            logger.error(f"Failed to upload file: {e}")
            raise

    def get_file(self, file_name):
        """Retrieve a file from the GenAI File API."""
        try:
            response = genai.get_file(name=file_name)
            logger.info(f"Retrieved file {response.display_name} as: {response.uri}")
            return response
        except Exception as e:
            logger.error(f"Failed to retrieve file: {e}")
            raise

    def delete_file(self, file_name):
        """Delete a file from the GenAI File API."""
        try:
            genai.delete_file(name=file_name)
            logger.info(f"Deleted file {file_name}")
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            raise

    def generate_content(self, content):
        """Generate content using Gemini 1.5 API LLM."""
        try:
            prompt = (
                "As a professional environmental and financial consultant, review the provided report. "
                "Please provide your analysis only in Markdown format. Summarize the key points, assess the short and long-term environmental impacts, "
                "evaluate the proposed solutions for preserving the environment, and discuss "
                "both the immediate and long-term benefits of these solutions. Refer to "
                "all text and image URLs content detailed in the following JSON structure for a thorough review."
            )            
            combined_text = prompt + "\n\Report Content:\n" + content
            model_name = "models/gemini-1.5-pro-latest"
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(combined_text)
            
            # Calculate the byte size of the response
            byte_size = len(response.encode('utf-8'))  # Encode and calculate bytes
            logger.info(f"Generated {byte_size} bytes of content.")

            return response
        except Exception as e:
            logger.error(f"Failed to generate content: {e}")
            raise
