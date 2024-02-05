from flask import Blueprint, request
from src.services.request_service import RequestService

request_route = Blueprint('request_route', __name__)

# Rutas CRUD para el modelo Request
request_route.route('/requests', methods=['POST'])
def create_request():
    data = request.get_json()
    return RequestService.create_request(data['name'], data['last_name'], data['status'], data['duration'])

request_route.route('/requests', methods=['GET'])
def get_all_requests():
    return RequestService.get_all_requests()

request_route.route('/requests/<int:request_id>', methods=['GET'])
def get_request_by_id(request_id):
    return RequestService.get_request_by_id(request_id)

request_route.route('/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    data = request.get_json()
    return RequestService.update_request(request_id, data['name'], data['last_name'], data['status'], data['duration'])

request_route.route('/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    return RequestService.delete_request(request_id)

