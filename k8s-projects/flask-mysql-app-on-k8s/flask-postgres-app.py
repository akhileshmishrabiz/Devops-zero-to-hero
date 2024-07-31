import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL configurations
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    user_email = db.Column(db.String(100), unique=True)
    user_password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.user_name = name
        self.user_email = email
        self.user_password = password

@app.route("/")
def index():
    """Function to test the functionality of the API"""
    return "Hello, world!"

@app.route("/create", methods=["POST"])
def add_user():
    """Function to add a user to the PostgreSQL database"""
    json = request.json
    name = json.get("name")
    email = json.get("email")
    pwd = json.get("pwd")
    
    if name and email and pwd:
        new_user = User(name, email, pwd)
        try:
            db.session.add(new_user)
            db.session.commit()
            resp = jsonify("User added successfully!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            db.session.rollback()
            return jsonify(str(exception)), 500
    else:
        return jsonify("Please provide name, email, and pwd"), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
