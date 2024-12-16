from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User , ServiceProvider


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

   
    new_user = User(
        name=data['name'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role=data['role']
    )
    db.session.add(new_user)
    db.session.commit()

    
    if data['role'] == 'provider':
        new_provider = ServiceProvider(
            id=new_user.id,  # Link the user_id
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(new_provider)
        db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


@auth.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        # Create access token with user ID as identity (string) and role as an additional claim
        access_token = create_access_token(
            identity=str(user.id),  # identity should be the user ID as a string
            additional_claims={"role": user.role}  # Include role as an additional claim
        )
        
        return jsonify({"access_token": access_token, "role": str(user.role)}), 200
    
    return jsonify({"message": "Invalid credentials"}), 401

