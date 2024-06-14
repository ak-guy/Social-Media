from flask import request
from user_utils.utils import (
    fetch_user_details, 
    make_user, 
    update_user_data, 
    delete_user,
    check_user
)
from src import create_app
import json


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

app = create_app()

@app.route('/signup-user', methods=('POST','GET'))
def signup():
    if request.method == 'GET':
        return "Get request working", 200
    
    if request.method == 'POST':
        data = request.get_json()
        status, error = make_user(data)
        if error:
            return 'Error', 404
        return 'Created', 201
    
@app.route('/get-users', methods=('GET', 'POST',))
def get_user():
    if request.method == 'GET':
        q_params = request.args
        print(f'q_parameters for get users >> {q_params}', flush=True)
        response = fetch_user_details(q_params)
        if not response:
            return 'Could not fetch user', 404
        return response, 200
    if request.method == 'POST':
        print(f'post hit to /get-users in user svc')
        auth = request.authorization
        user_column, value = auth.username.split('---')
        password = auth.password
        does_exists = check_user(user_column, value, password)
        print(f'does_exists = {does_exists}', flush=True)
        if does_exists:
            return "User Exists", 200
        
        return "User does not exist", 404
        

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