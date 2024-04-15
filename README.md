# Google Hackathon API

## Get started (Running locally)

### Prerequisites:

Python and Pip will need to be installed on your machine. You will also need to create a Google Gemini API key.

### Create and activate the virtual environment:

```
python -m venv venv
.\venv\Scripts\activate
```

### Install dependencies:

```
pip install -U -r requirements.txt
```

### Create a .env file in the root of the project folder:

```
# FLASK_ENV - can be "development" for console logging or "production" for logging to a file (defined in ./services/logger.py).
# SECRET_KEY - Needs to match the key set in the application within the client .env file.
# PORT - Needs to match the port set in the application within the client .env file.
# GOOGLE_API_KEY - Your unique Google Gemini Key


FLASK_ENV=development 
SECRET_KEY=super_secret_key
IP_ADDRESS=0.0.0.0 
PORT=5000
GOOGLE_API_KEY = XXXXX
```

### Run the API:

```
python app.py
```

### Testing the endpoints:

The API needs to be running in separate terminal to test.

```
pytest -s ./tests/test_endpoints.py
```