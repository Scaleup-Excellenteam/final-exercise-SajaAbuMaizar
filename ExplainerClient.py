import requests


class WebApiClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url

    def upload_file(self, filename, email=None):
        url = f'{self.base_url}/upload'
        files = {'file': open(filename, 'rb')}
        data = {'email': email} if email else None

        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print('Upload successful.')
            uid = response.json()['uid']
            self.process_presentation(uid)
        else:
            print('Upload failed.')

    def process_presentation(self, uid):
        url = f'{self.base_url}/process_presentation/{uid}'

        response = requests.get(url)
        if response.status_code == 200:
            print('Presentation processed successfully.')
        else:
            print('Failed to process presentation.')

    def check_status(self, uid):
        url = f'{self.base_url}/status/{uid}'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print('Status:', data['status'])
            print('Filename:', data['filename'])
            print('Upload Time:', data['upload_time'])
            print('Finish Time:', data['finish_time'])
            print('User ID:', data['user_id'])
        else:
            print('Failed to retrieve status.')

    def view_history(self):
        url = f'{self.base_url}/history'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for upload in data:
                print('UID:', upload['uid'])
                print('Filename:', upload['filename'])
                print('Status:', upload['status'])
                print('Upload Time:', upload['upload_time'])
                print('Finish Time:', upload['finish_time'])
                print('User ID:', upload['user_id'])
                print('--------------------')
        else:
            print('Failed to retrieve upload history.')


if __name__ == '__main__':
    client = WebApiClient()
    client.upload_file('example.pptx', email='user@example.com')
    client.check_status('uid123')
    client.view_history()
