import google.generativeai as genai
import os
import json
from services.logger import logger

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.env_variable = os.getenv('ENV')

        # Initialize Google API Client
        genai.configure(api_key=self.api_key)
        logger.info("Initialized Google Generative AI API client with provided API key.")

    def upload_file(self, file_name, display_name):
        """Upload a file to the GenAI File API."""
        file_path = "temp/" + file_name
        try:
            if self.env_variable == 'production':
                response = genai.upload_file(path=file_path, display_name=display_name)
                logger.info(f"Successfully uploaded file '{display_name}' to GenAI File API at: {response.uri}")
                return response.uri
            else:
                logger.info(f"Simulated upload for '{display_name}' in development mode at: {file_path}")
                return file_path
        except Exception as e:
            logger.error(f"Failed to upload file '{display_name}': {e}")
            raise

    def get_file(self, file_name):
        """Retrieve a file from the GenAI File API."""
        try:
            response = genai.get_file(name=file_name)
            logger.info(f"Successfully retrieved file '{file_name}' from GenAI File API.")
            return response
        except Exception as e:
            logger.error(f"Failed to retrieve file '{file_name}': {e}")
            raise

    def delete_file(self, file_name):
        """Delete a file from the GenAI File API."""
        try:
            genai.delete_file(name=file_name)
            logger.info(f"Successfully deleted file '{file_name}' from GenAI File API.")
        except Exception as e:
            logger.error(f"Failed to delete file '{file_name}': {e}")
            raise

    def generate_content(self, content):
        try:
            prompt = (
                "I need you to be an environment and financial professional advisor. "
                "Can you review the text that follows? Analyze what it's about and assess each of the images. "
                "Based on the text (with insight of the images) determine specific short/long term negative impacts "
                "to the environment. Provide meaningful green solutions, and determine the specific short and long term "
                "benefits of those solutions. I need the response to be in Markdown form."
            )
            combined_text = f"{prompt}\nReport Content:\n{content}"
            model_name = "gemini-pro"
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(combined_text)
            response_text = response.text  # assuming response object has a 'text' attribute
            
            byte_size = len(response_text.encode('utf-8'))
            logger.info(f"Generated content of {byte_size} bytes successfully.")

            return response_text
        except Exception as e:
            logger.error(f"Failed to generate content: {e}")
            raise
