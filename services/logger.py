import logging
import os
from dotenv import load_dotenv

#load_dotenv()

def setup_logger(name='Logger', level=logging.INFO, log_file='app.log'):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Determine the output handler based on the FLASK_ENV environment variable
    if os.getenv('VERBOSE') == 'false':
        handler = logging.FileHandler(log_file)  # Log to file in production
    else:
        handler = logging.StreamHandler()  # Log to console in non-production environments

    # Format the text output in logs
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

# Setup the logger
logger = setup_logger()
