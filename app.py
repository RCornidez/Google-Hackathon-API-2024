from flask import Flask
from flask_socketio import SocketIO
from components import endpoints
from services.logger import logger
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize SocketIO with CORS enabled
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize endpoints
endpoints.init_app(app, socketio)

if __name__ == '__main__':
    logger.info("Starting Flask API server")
    ip_address = os.getenv('IP_ADDRESS')
    port = int(os.getenv('PORT'))
    socketio.run(app, host=ip_address, port=port)
