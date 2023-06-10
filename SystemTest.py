import os
import subprocess
import time
from datetime import datetime
import requests
import WebAPI
import Explainer
from ExplainerClient import WebApiClient

# Start the Web API
web_api_process = subprocess.Popen(['python', 'WebAPI.py'])
time.sleep(2)  # Wait for the Web API to start

# Start the Explainer
explainer_process = subprocess.Popen(['python', 'Explainer.py'])

# Wait for the Explainer to initialize
time.sleep(2)

# Create a Python API client instance
api_client = WebApiClient('http://localhost:5000')

try:
    # Upload a sample presentation
    presentation_path = 'sample.pptx'  # change to your sample
    uid = api_client.upload(presentation_path)
    print(f"Uploaded presentation. UID: {uid}")

    # Check the status of the presentation
    status = api_client.status(uid)
    if status.is_done():
        print("Status: Done")
        print(f"Explanation: {status.explanation}")
    else:
        print("Status: Pending")
        print("Waiting for the processing to complete...")

finally:
    # Stop the Explainer
    explainer_process.terminate()

    # Stop the Web API
    web_api_process.terminate()

    # Wait for the processes to stop
    explainer_process.wait()
    web_api_process.wait()
