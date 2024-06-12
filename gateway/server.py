from flask import Flask, request, Response
from pydantic import (
    BaseModel, 
    EmailStr,
    field_validator
)
import ast
from user_svc.user_comm import create_user, get_user_details, update_resource
from user_svc.utils import user_details_handler
import json

app = Flask(__name__)

'''
test curl command : 
1. testing signup
curl -X POST -H "Content-Type: text/html;" http://127.0.0.1:8080/signup -d "{'name': 'Arpit', 'username': 'ak_guy', 'email': 'test@gmail.com', 'password': 'test1234', 'phone_number': '+91-1234567890'}" 

2. testing get user with user_id
curl -X GET -H "Content-Type: text/html;" "http://127.0.0.1:8080/get-user?name=arpit&limit=1"

3. testing deleting and updating user
curl -X PATCH -H "Content-Type: text/html;" "http://127.0.0.1:8080/update_user/1 -d "{'name': 'Arpit Kumar'}"
'''

class User(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    phone_number: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password Length must be greater that 8")
        
        return value
        
    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value):
        country_code, actual_number = value.split('-')
        if len(actual_number) != 10:
            raise ValueError("Phone number should be exactly 10 digits")
        
        return value
        

@app.route("/signup", methods=("POST",))
def signup_user():
    if request.method == 'POST':
        data = ast.literal_eval(request.data.decode('ascii'))
        user_obj = User(**data)
        msg, error = create_user(user_obj.model_dump())
        if not error:
            return {'Success': True, 'Message': 'User created'}, 201
        
        return {'Success': False, 'Message': 'User could not be created'}, 401

@app.route("/update_user/<int:user_id>", methods=("PATCH", "DELETE"))
def update_user(user_id):
    if request.method == 'PATCH' or request.method == 'DELETE':
        # user_id = request.args.get('user_id')
        data = request.data if request.method == 'PATCH' else None
        if not user_id:
            return "Incorrect Url", 404
        
        msg, error = update_resource(user_id, data, method=request.method)
        update_or_delete = 'Updated' if request.method == 'PATCH' else 'Deleted'
        if not error:
            return f'User {update_or_delete} !!', 200
        
        return msg, 404

@app.route('/get-user', methods=('GET',))
def user_detail():
    if request.method == 'GET':
        query_parameters = request.args
        response, error = user_details_handler(query_parameters)
        if not error:
            return response, 200

        return {'Success': False, 'Message': 'Failed to fetch user'}, 404
    

if __name__ == '__main__':
    app.run(debug=True, port=8080)