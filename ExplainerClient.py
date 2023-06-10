import requests
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: str

    def is_done(self):
        return self.status == 'done'


class WebApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        url = f"{self.base_url}/upload"

        with open(file_path, 'rb') as file:
            response = requests.post(url, files={'file': file})

        if response.status_code == 200:
            json_response = response.json()
            uid = json_response.get('uid')
            if uid:
                return uid
            else:
                raise Exception("Invalid response: missing UID")
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def status(self, uid):
        url = f"{self.base_url}/status/{uid}"

        response = requests.get(url)

        if response.status_code == 200:
            json_response = response.json()
            status = json_response.get('status')
            filename = json_response.get('filename')
            timestamp = json_response.get('timestamp')
            explanation = json_response.get('explanation')

            if status and filename and timestamp:
                timestamp = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
                return Status(status, filename, timestamp, explanation)
            else:
                raise Exception("Invalid response: missing required fields")
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")


if __name__ == '__main__':
    # Example usage
    client = WebApiClient("http://localhost:5000")  # Replace with the appropriate base URL

    try:
        uid = client.upload("hello.pptx")
        print(f"Upload successful. UID: {uid}")

        status = client.status(uid)
        if status.is_done():
            print("Status: Done")
            print(f"Explanation: {status.explanation}")
        else:
            print("Status: Pending")
            print("Waiting for the processing to complete...")
    except Exception as e:
        print(f"Error: {str(e)}")
