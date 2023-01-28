import os

import requests
from dotenv import load_dotenv
load_dotenv()

CURATEIT_URL = os.getenv('CURATEIT_URL')
CURATEIT_AUTH_TOKEN = os.getenv('CURATEIT_AUTH_TOKEN')

def save_image(file_name: str, file_path: str, file_mime_type: str) -> int:
    '''
    Save the file to server

    Parameters:
        - file_name(str)
        - file_path(str)
        - file_mime_type
    
    Returns:
        - status code of the request
    '''

    url = f'{CURATEIT_URL}/imageocr?openai=true&imageColor=true'
    files=[
    ('image', (file_name, open(file_path,'rb'), file_mime_type))
    ]
    headers = {
    'Authorization': f'Bearer {CURATEIT_AUTH_TOKEN}'
    }
    response = requests.request('POST', url, headers=headers, files=files)
    
    return response.status_code

def save_pdf(file_name: str, file_path: str, file_mime_type: str) -> int:
    '''
    Save the file to server

    Parameters:
        - file_name(str)
        - file_path(str)
        - file_mime_type
    
    Returns:
        - status code of the request
    '''

    url = f'{CURATEIT_URL}/imageocr?openai=true&imageColor=true'
    files=[
    ('file', (file_name, open(file_path,'rb'), file_mime_type))
    ]
    headers = {
    'Authorization': f'Bearer {CURATEIT_AUTH_TOKEN}'
    }
    response = requests.request('POST', url, headers=headers, files=files)
    
    return response.status_code