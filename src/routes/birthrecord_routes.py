from flask import Blueprint, render_template, request, jsonify
from src.models.birthrecord_model import db
from src.services.birthrecord_service import save_birth_record
from datetime import datetime

birthrecord_route = Blueprint('birthrecord_route', __name__)

@birthrecord_route.route('/')
def index():
    return render_template('home.html')

@birthrecord_route.route('/save_record', methods=['POST'])
def save_record():
    try:
        data = request.get_json() 
        record_number = data['record_number']
        names = data['names']
        birth_date = data['birth_date']
        birth_time = data['birth_time']
        place_birth = data['place_birth']

        success, error_message = save_birth_record(record_number, names, birth_date, birth_time, place_birth)

        if success:
            return jsonify({"message": "Record saved successfully"}), 200
        else:
            return jsonify({"error": f"Error saving record: {error_message}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error in request: {str(e)}"}), 400


