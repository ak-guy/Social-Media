import requests
import os
from dotenv import load_dotenv

load_dotenv()

USER_PORT_NUMBER = os.environ.get('USER_PORT_NUMBER')

def create_user(data_obj):
    url = f'http://localhost:{USER_PORT_NUMBER}/signup-user'
    conn = requests.post(url, json=data_obj)
    if conn.status_code == 201:
        return conn.text, None
    
    return conn.text, conn.status_code

def get_user_details(pk: int):
    pass


def update_resource(user_id, data, method):
    url = f'http://localhost:{USER_PORT_NUMBER}/update-user/{user_id}'
    if method == 'PATCH':
        conn = requests.patch(url, json=data)
    else:
        conn = requests.delete(url)
    if conn.status_code == 201:
        return conn.text, None
    
    return conn.text, conn.status_code