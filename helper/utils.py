import os

from helper.telegram_api import get_file_path, save_file_and_get_local_path
from helper.curateit_api import save_image
from helper.openai_api import text_complition


def process_telegram_data(data: dict) -> dict:

    is_text = False
    is_photo = False
    is_document = False
    is_unknown = True

    sender_id = ''
    text = ''
    file_id = ''
    mime_type = ''

    if 'message' in data.keys():
        message = data['message']
        sender_id = message['from']['id']
        if 'text' in message.keys():
            text = message['text']
            is_text = True
            is_unknown = False
        if 'photo' in message.keys():
            file_id = message['photo'][len(message['photo'])-1]['file_id']
            is_photo = True
            is_unknown = False
        if 'document' in message.keys():
            file_id = message['document']['file_id']
            mime_type = message['document']['mime_type']
            is_document = True
            is_unknown = False

    return {
        'is_text': is_text,
        'is_photo': is_photo,
        'is_document': is_document,
        'is_unknown': is_unknown,
        'sender_id': sender_id,
        'text': text,
        'file_id': file_id,
        'mime_type': mime_type
    }


def generate_text_response(text: str) -> str:

    if text == '/start':
        return 'Hi, I can help you with saving your data to the cloud and retive it, I can also help you with your questions.'
    if text == '/image':
        return 'Select the image file that you want to save.'
    if text == '/file':
        return 'Select the document file that you want to save.'
    if text == '/help':
        return 'I am an AI and I am here to help you. Please enter a command or ask me a question for more information.'

    result = text_complition(text)

    if result['status'] == 1:
        return result['response'].strip()
    else:
        return 'We are facing some technical issue.'


def generate_image_response(file_id: str) -> str:

    file_path = get_file_path(file_id)

    if file_path['status'] == 1:
        local_file_path = save_file_and_get_local_path(file_path['file_path'])

        if local_file_path['status'] == 1:
            status_code = save_image(
                local_file_path['file_name'], local_file_path['local_file_path'], f'image/{local_file_path["extension"]}')
            os.unlink(local_file_path['local_file_path'])
            if status_code == 200:
                return 'File saved successfully.'
            else:
                return 'We are facing some technical issue.'


def generate_file_response(file_id: str, mime_type: str) -> str:

    file_path = get_file_path(file_id)

    if file_path['status'] == 1:
        local_file_path = save_file_and_get_local_path(file_path['file_path'])

        if local_file_path['status'] == 1:
            status_code = save_image(
                local_file_path['file_name'], local_file_path['local_file_path'], mime_type)
            os.unlink(local_file_path['local_file_path'])
            if status_code == 200:
                return 'File saved successfully.'
            else:
                return 'We are facing some technical issue.'
