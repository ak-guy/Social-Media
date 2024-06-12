from abc import ABC, abstractmethod
import requests
from dotenv import load_dotenv
import os

load_dotenv()

USER_PORT_NUMBER = os.environ.get('USER_PORT_NUMBER')


class UrlGenerator:
    @staticmethod
    def generate_url(q_params):
        base_url = f'http://localhost:{USER_PORT_NUMBER}/get-users'
        if 'user_id' in q_params:
            base_url += f'?user_id={q_params.get("user_id")}'
            return base_url
        elif 'username' in q_params:
            base_url += f'?username={q_params.get("username")}'
            return base_url
        elif 'name' in q_params:
             base_url += f'?name={q_params.get("name")}'
            
        if 'limit' in q_params:
            base_url += f'&limit={q_params.get("limit")}'
        elif 'offset' in q_params:
            base_url += f'&offset={q_params.get("offset")}'

        return base_url

class IUserDetails(ABC):
    @abstractmethod
    def handleUserApi(self):
        pass

class SearchUser(IUserDetails):
    def handleUserApi(self, q_params):
        url = UrlGenerator.generate_url(q_params)
        conn = requests.get(url)
        if conn.status_code == 200:
            return conn.text, None
        
        return conn.text, conn.status_code
    
def user_details_handler(q_params: dict) -> tuple[str, int]:
    handler_obj: IUserDetails = SearchUser()
    response, status_code = handler_obj.handleUserApi(q_params)
    return response, status_code