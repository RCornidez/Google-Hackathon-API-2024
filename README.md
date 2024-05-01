# Trees Bees & Seas Flask API

See our submission on DevPost =>

See our presentation on YouTube =>

See the Flutter application that uses this API => https://github.com/RCornidez/Google-Hackathon-2024

## Table of Contents
<ul>
    <li><a href="#how">How-to-run</a></li>
    <li><a href="#files">Folders and files relevant to the project</a></li>
    <li><a href="#env">.env file setup</a></li>

</ul>

<h3 id="how"> How-to-run: </h3>

```
## Prerequisites:
1. Python, Pip, and Git will need to be installed on your system.
2. Install WeasyPrint's dependencies based on your system (This is necessary for PDF file creation).
    Installation instructions: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation
3. Create a Google Gemini API key.
4. Create a .env file in the root of the folder based on the example below.

# Clone the git repository
git clone https://github.com/RCornidez/Google-Hackathon-API-2024.git

# Create and activate the virtual environment:
python -m venv venv
.\venv\Scripts\activate

# Install dependencies:
pip install -U -r requirements.txt

# Run the API
python app.py

# Testing the endpoints (The API needs to be running in a separate terminal to test)
# in the second terminal run:
pytest -s ./tests/test_endpoints.py

# you can see the documents created within the temp directory and the sample input and output within tests/samples

```

<h3 id="files"> Folders and files relevant to the project: </h3>

```
/ Trees Bees & Seas Flask API
|-- components/
|   |-- templates                   # HTML template for the PDF environmental report sent to the client 
|   |-- endpoints.py                # The API routes are defined here
|-- services/
|   |-- gemini.py                   # Class for interacting with the Google Gemini API
|   |-- logger.py                   # Class for formatting and controlling the API log output
|   |-- pdf.py                      # Class for handling incoming and outgoing files
|-- temp/                           # Temporary folder where all documents and files are stored
|-- tests/
|   |-- samples/                    # Contains a sample report and output directory when testing the endpoints                          
|   |-- test_endpoints.py           # Simulation of client request for all endpoints
|-- app.log                         # logfile that is automatically created when VERBOSE=false is set in .env
|-- app.py                          # Main application file used to initialize the .env variables, logger, and API routes
|-- requirements.txt                # dependencies list
```

<h3 id="env"> Create a .env file in the root of the project folder: </h3>

```
'''
ENV - can be:
    development - for testing uploads locally with sample responses.
    production - uploading to Gemini File API and Gemini AI API
VERBOSE - can be:
    false - to log output to a file (defined in services/logger.py)
    true - to log output to console
PORT - Needs to match the port set in the application within the client .env file.
IP_ADDRESS - 0.0.0.0 to run on all addresses of the host, otherwise set a specific address.
GOOGLE_API_KEY - Your unique Gemini Key, not needed if testing in development mode.
'''

ENV=development
VERBOSE=false
PORT=5000
IP_ADDRESS=0.0.0.0
GOOGLE_API_KEY = XXXXX
```

