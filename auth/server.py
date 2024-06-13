from flask import Flask, request
import jwt

app = Flask(__name__)

@app.route("/user-login", methods=('POST',))
def login():
    auth = request.authorization
    print(f"username = {auth.username}, password = {auth.password}", flush=True)
    return "logged in", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)