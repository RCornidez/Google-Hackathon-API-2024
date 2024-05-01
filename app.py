from flask import Flask
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Import internal components
try:
    from components import endpoints
    from services.logger import logger
except ImportError as e:
    sys.exit(f"Failed to import components or services: {e}")

app = Flask(__name__)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize endpoints
try:
    endpoints.init_app(app, socketio)
except Exception as e:
    logger.error(f"Failed to initialize endpoints: {e}")
    sys.exit(1)

if __name__ == '__main__':
    ip_address = os.getenv('IP_ADDRESS')
    if not ip_address:
        logger.error("IP_ADDRESS environment variable not set.")
        sys.exit(1)

    port = os.getenv('PORT')
    if not port:
        logger.error("PORT environment variable not set.")
        sys.exit(1)
    try:
        port = int(port)
    except ValueError:
        logger.error(f"Invalid PORT value: {port}")
        sys.exit(1)

    logger.info("Starting Flask API server")
    try:
        socketio.run(app, host=ip_address, port=port, debug=True)
    except Exception as e:
        logger.error(f"Failed to start the Flask API server: {e}")
        sys.exit(1)
