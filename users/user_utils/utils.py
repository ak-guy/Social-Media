from __future__ import annotations
from abc import ABC, abstractmethod
from models import Users
from src import db
import json
# from sqlalchemy.sql.elements import literal_column
from sqlalchemy import literal_column, select
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
    def getUserInfo(self, q_params, get_password=False):
        user_id = q_params.get('user_id')
        user_details = Users.query.filter_by(id=user_id).first()

        if not user_details:
            return None
        data = {
            'id': user_details.id,
            'name': user_details.name,
            'username': user_details.username,
            'email': user_details.email,
            'created_on': user_details.created_on,
            'phone_number': user_details.phone_number
        }
        if get_password:
            data.update({'password': user_details.password})
        return data

def fetch_user_details(q_params: dict) -> tuple[str, int]:
    handler_obj: IUserDetails = Builder().createUserDetailsObj(q_params)
    response = handler_obj.getUserInfo(q_params)

    return response

def make_user(data):
    try:
        user = Users(name=data.get('name'), username=data.get('username'), email=data.get('email'), password=data.get('password'), phone_number=data.get('phone_number'))
        db.session.add(user)
        db.session.commit()
        return 'Created', None
    except Exception as e:
        return f'Could not create user', e
    
def delete_user(user_id):
    row_to_delete = Users.query.filter_by(id=user_id).first()
    if row_to_delete:
        db.session.delete(row_to_delete)
        db.session.commit()
        return "User Deleted Successfully", 200
    return "User not found", 404
            
def update_user_data(user_id, data):
    user_obj = SearchUserInDBByUserID()
    actual_user_data = user_obj.getUserInfo({'user_id': user_id}, get_password=True)

    row_to_update = Users.query.filter_by(id=user_id).first()
    if row_to_update:
        row_to_update.name = data.get('name', actual_user_data.get('name'))
        row_to_update.username = data.get('username', actual_user_data.get('username'))
        row_to_update.email = data.get('email', actual_user_data.get('email'))
        row_to_update.phone_number = data.get('phone_number', actual_user_data.get('phone_number'))
        row_to_update.password = data.get('password', actual_user_data.get('password'))
        db.session.commit()
        return "User details updated", 200
    
    return "User not found", 404

class IUserValidator:
    pass

def check_user(user_column: str, value: str, password: str):
    try:
        # does not work (check login api)
        user_exists = db.session.execute(db.select(Users).filter_by(literal_column(user_column)==value)).scalar_one()
        return user_exists
    except Exception as e:
        print(f'Exception while getting user {e}')
        return False
