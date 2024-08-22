import requests
import base64
from flask import Flask, render_template

GITHUB_TOKEN = 'my_token'
REPO = 'Ananda-001/location-data'
LOCATION_FILE_PATH = 'location.txt'
DATA_FILE_PATH = 'data.txt'

def get_file_content(file_path):
    url = f'https://api.github.com/repos/{REPO}/contents/{file_path}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        if 'content' in json_response:
            content = base64.b64decode(json_response['content']).decode('utf-8')
            return content
        else:
            print(f"Key 'content' not found in the response for {file_path}.")
            return None
    elif response.status_code == 404:
        print(f"File {file_path} not found. Status Code: 404")
        return None
    else:
        print(f"Failed to fetch file content for {file_path}. Status Code: {response.status_code}")
        return None

def get_location():
    content = get_file_content(LOCATION_FILE_PATH)
    if content:
        lat, lon = map(float, content.split(','))
        return lat, lon
    else:
        return None, None

def get_data():
    content = get_file_content(DATA_FILE_PATH)
    if content:
        data = {}
        for line in content.split('\n'):
            key, value = line.split(': ')
            data[key] = value
        return data
    else:
        return {}

app = Flask(__name__)

@app.route('/')
def home():
    lat, lon = get_location()
    data = get_data()
    return render_template('data.html', lat=lat, lon=lon, data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
