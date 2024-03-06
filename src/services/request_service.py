from flask_sqlalchemy import SQLAlchemy
from src.models.request_model import db, Request
from flask import jsonify

class RequestService:
    @staticmethod
    def create_request(act_number, name, last_name, status):
        new_request = Request(act_number=act_number, name=name, last_name=last_name, status=status)
        db.session.add(new_request)
        db.session.commit()
    
    @staticmethod
    def get_all_requests():
        requests = Request.query.all()
        result = []
        for request in requests:
            result.append({
                "id": request.id,
                "name": request.name,
                "last_name": request.last_name,
                "status": request.status,
                "act_number": request.act_number
            })
        return result

    @staticmethod
    def get_request_by_id(request_id):
        request = Request.query.get(request_id)
        if request:
            return {
                "id": request.id,
                "name": request.name,
                "last_name": request.last_name,
                "duration": request.duration,
            }
        else:
            return None

    @staticmethod
    def update_request(request_id, status):
        request = Request.query.get(request_id)
        if request:
            request.status = status
            db.session.commit()
            return jsonify({"message": "Request updated successfully"})
        else:
            return jsonify({"error": "Request not found"})

    @staticmethod
    def delete_request(request_id):
        request = Request.query.get(request_id)
        if request:
            db.session.delete(request)
            db.session.commit()
            return jsonify({"message": "Request deleted successfully"})
        else:
            return jsonify({"error": "Request not found"})
