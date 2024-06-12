from __future__ import annotations
from abc import ABC, abstractmethod
from models import Users
from src import db
import json

class Builder:
    def createUserDetailsObj(self, q_params) -> IUserDetails:
        if 'user_id' in q_params:
            return SearchUserInDBByUserID()
        elif 'name' in q_params:
            return SearchUserInDBByName()
        elif 'username' in q_params:
            return SearchUserInDBByUsername()
        else:
            ValueError("Incorrect url !!!")

class IUserDetails(ABC):
    @abstractmethod
    def getUserInfo(self):
        pass

class SearchUserInDBByName(IUserDetails):
    def getUserInfo(self, q_params):
        name = q_params.get('name')
        user_details = Users.query.filter_by(name=name)
        if 'limit' in q_params:
            user_details = user_details.limit(int(q_params.get('limit')))
        if 'offset' in q_params:
            user_details = user_details.offset(q_params.get('offset'))
        
        if not user_details:
            return None
        
        response = []
        for user_detail in user_details:
            data = {
                'id': user_detail.id,
                'name': user_detail.name,
                'email': user_detail.email,
                'created_on': str(user_detail.created_on),
                'username': user_detail.username
            }
            response.append(data)
        response = json.dumps(response)
        return response

class SearchUserInDBByUsername(IUserDetails):
    def getUserInfo(self, q_params):
        username = q_params.get('username')
        user_details = Users.query.filter_by(username=username).first()
        if not user_details:
            return None
        
        data = {
            'id': user_details.id,
            'name': user_details.name,
            'email': user_details.email,
            'created_on': user_details.created_on
        }
        return data
    
class SearchUserInDBByUserID(IUserDetails):
    def getUserInfo(self, q_params):
        user_id = q_params.get('user_id')
        user_details = Users.query.filter_by(id=user_id).first()

        if not user_details:
            return None
        data = {
            'id': user_details.id,
            'name': user_details.name,
            'email': user_details.email,
            'created_on': user_details.created_on,
            'username': user_details.username
        }
        return data

def fetch_user_details(q_params: dict) -> tuple[str, int]:
    handler_obj: IUserDetails = Builder().createUserDetailsObj(q_params)
    response = handler_obj.getUserInfo(q_params)
    print(f'fetch user details in user service >> {response}', flush=True)
    return response

def make_user(data):
    try:
        user = Users(name=data.get('name'), username=data.get('username'), email=data.get('email'), password=data.get('password'), phone_number=data.get('phone_number'))
        db.session.add(user)
        db.session.commit()
        return 'Created', None
    except Exception as e:
        return f'Could not create user', e
    
def update_user_data(user_id, data=None):
    if not data:
        row_to_delete = Users.query.filter(id=user_id).first()
        if row_to_delete:
            db.session.delete(row_to_delete)
            db.session.commit()
            return "User Deleted Successfully", 200
    
    print(data, flush=True)
            