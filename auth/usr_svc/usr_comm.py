import requests
from dotenv import load_dotenv
import os

load_dotenv()

USER_PORT_NUMBER = os.environ.get('USER_PORT_NUMBER')

def make_user_request(username, password):
    url = f'http://localhost:{USER_PORT_NUMBER}/get-users'
    print(f'pinging user svc from auth svc with url >> {url}', flush=True)
    auth = (username, password)
    conn = requests.post(
        url, auth=auth
    )
    
    if conn.status_code == 200:
        return "User Logged in !!", 200
    
    return conn.text, 404