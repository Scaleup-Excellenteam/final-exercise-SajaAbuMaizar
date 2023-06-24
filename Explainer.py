import requests
from presentation_processor import PresentationProcessor


def upload_file(filename, email=None):
    url = 'http://localhost:5000/upload'
    files = {'file': open(filename, 'rb')}
    data = {'email': email} if email else None

    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        print('Upload successful.')
        uid = response.json()['uid']
        process_presentation(uid)
    else:
        print('Upload failed.')


def process_presentation(uid):
    url = f'http://localhost:5000/process_presentation/{uid}'

    response = requests.get(url)
    if response.status_code == 200:
        print('Presentation processed successfully.')
    else:
        print('Failed to process presentation.')


def check_status(uid):
    url = f'http://localhost:5000/status/{uid}'

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


def view_history():
    url = 'http://localhost:5000/history'

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
    upload_file('example.pptx', email='user@example.com')
    check_status('uid123')
    view_history()
