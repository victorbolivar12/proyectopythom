from src.models.users_model import User
from src.models.request_model import db
from flask import jsonify

class UserService:
    @staticmethod
    def create_user(email, password, rol):
        new_user = User(email=email, password=password, rol=rol)
        db.session.add(new_user)
        db.session.commit()
    
    @staticmethod
    def get_all_users():
        users = User.query.all()
        result = []
        for user in users:
            result.append({
                "id": user.id,
                "email": user.email,
                "rol": user.rol
            })
        return result

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if user:
            return {
                "id": user.id,
                "email": user.email,
            }
        else:
            return None

    @staticmethod
    def update_user(user_id, email, password):
        user = User.query.get(user_id)
        if user:
            user.email = email
            user.password = password
            db.session.commit()
            return jsonify({"message": "User updated successfully"})
        else:
            return jsonify({"error": "User not found"})

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"})
        else:
            return jsonify({"error": "User not found"})
