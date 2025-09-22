from flask import Blueprint, jsonify
from flask_cors import cross_origin
from src.models.user import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@cross_origin()
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())