from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import Users
from app.schemas import user_schema
from app import db, mail
from flask_mail import Message

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if Users.query.filter_by(email=data['email']).first():
        return jsonify({"message": "User already exists"}), 409
    user = Users(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = Users.query.filter_by(email=data['email'], password=data['password']).first()
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401
    access_token = create_access_token(identity=user.email)
    return jsonify(access_token=access_token)

@users_bp.route('/forgot_password/<string:email>', methods=['GET'])
def forgot_password(email):
    user = Users.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Email not found"}), 404
    msg = Message(
        subject="Your Password",
        sender="admin@planetary-api.com",
        recipients=[email],
        body=f"Your password is: {user.password}"
    )
    mail.send(msg)
    return jsonify({"message": "Password sent to your email"})
