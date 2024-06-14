from flask import Flask, request
import jwt
from usr_svc.usr_comm import make_user_request


app = Flask(__name__)

@app.route("/user-login", methods=('POST',))
def login():
    if request.method == 'POST':
        auth = request.authorization

        if not auth:
            return "Invalid Credential !!", 404
        
        username = auth.username
        password = auth.password
        print(f"hit from gateway service to auth service came at /user-login")
        reponse, error_code = make_user_request(username, password)
        # print(f"username = {auth.username}, password = {auth.password}", flush=True)
        return reponse, error_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)