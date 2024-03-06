from flask import Blueprint, request
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, send_file

user_route = Blueprint('user_route', __name__)

user_route.route('/auth', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(username)
        print(password)
        return redirect(url_for('birthrecord_route.request_birthcertificate'))
