import requests
from dotenv import load_dotenv
import os
import ast

load_dotenv()

AUTH_PORT_NUMBER = os.environ.get('AUTH_PORT_NUMBER')

def make_login_request(data):
    '''
    return value -> (token, error)
    '''
    if not data:
        return None, ("Credential not found", 401)
    
    password = data.get('password')
    
    username = [key for key in data.keys() if key in ('username', 'email', 'phone_number')][0]
    # print(f'incomplete username = {username}', flush=True)
    username += f"---{data.get('username', data.get('email', data.get('phone_number')))}"
    # print(f'complete username = {username}', flush=True)

    auth = (username, password)
    url = f'http://localhost:{AUTH_PORT_NUMBER}/user-login'
    print(f'url = {url}')

    # will ping to auth service to get jwt token
    conn = requests.post(
        url, auth=auth
    )

    if conn.status_code == 200:
        return conn.text, None
    
    print(conn.text, flush=True)
    print(conn.status_code, flush=True)
    return None, (conn.text, conn.status_code)