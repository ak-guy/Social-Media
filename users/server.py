from flask import Flask, request
from ast import literal_eval
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from user_utils.utils import fetch_user_details, make_user, update_user_data, delete_user
from src import create_app
import json


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

app = create_app()

@app.route('/signup-user', methods=('POST','GET'))
def create_user():
    if request.method == 'GET':
        return "Get request working", 200
    
    if request.method == 'POST':
        data = request.get_json()
        status, error = make_user(data)
        if error:
            return 'Error', 404
        return 'Created', 201
    
@app.route('/get-users')
def get_user():
    if request.method == 'GET':
        q_params = request.args
        print(f'q_parameters for get users >> {q_params}', flush=True)
        response = fetch_user_details(q_params)
        if not response:
            return 'Could not fetch user', 404
        return response, 200

@app.route('/update-user/<int:user_id>', methods=('PATCH', 'DELETE'))
def update_user(user_id):
    if request.method == 'PATCH':
        data = json.loads(request.get_json())
        print(f"data type = {type(data)}, actual_data = {data}")
        msg, status = update_user_data(user_id, data)
        return msg, status
    
    if request.method == 'DELETE':
        msg, status = delete_user(user_id)
        return msg, status

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True, port=8000)