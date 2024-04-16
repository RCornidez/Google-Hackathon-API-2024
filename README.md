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
'''
ENV - can be:
    development - for testing uploads locally
    production - uploading to Gemini File API and Gemini AI API
VERBOSE - can be:
    false - to log output to a file (defined in services/logger.py)
    true - to log output to console
SECRET_KEY - Needs to match the SECRET_KEY set in the application within the client .env file.
PORT - Needs to match the port set in the application within the client .env file.
IP_ADDRESS - 0.0.0.0 to run on all addresses of the host, otherwise set a specific address.
GOOGLE_API_KEY - Your unique Gemini Key, not needed if testing in development mode.
'''

ENV=development
VERBOSE=false
SECRET_KEY=super_secret_key  
PORT=5000
IP_ADDRESS=0.0.0.0
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