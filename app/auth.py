from flask import Blueprint, request, render_template, redirect, url_for
from app.models.user import User
from app.models.violation import Violation
from app.shared import api_response, post_request_arguments
from flask_login import login_user, login_required, current_user, logout_user
import re

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET'])
def get_register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.get_profile'))

    return render_template('auth/register.html' , establishment_names=Violation.establishment_names())

@bp.route('/register', methods=['POST'])
def post_register():
    request_arguments = post_request_arguments(request)
    full_name = request_arguments['full_name']
    email = request_arguments['email']
    password = request_arguments['password']

    if not full_name or not email:
        return "Bad request", 400

    if not is_valid_email(email):
        return "Invalid email", 400

    if len(password) < 8:
        return "Password should be longer than 8 characters", 400
    
    new_user = User(full_name, email)
    new_user.register(password)
    login_user(new_user)

    if request.content_type == 'application/x-www-form-urlencoded':
        return redirect(url_for('auth.get_profile'))
    return api_response(new_user.to_dict(), request.content_type)
    
@bp.route('/login', methods=['GET'])
def get_login():
    return render_template('auth/login.html')

@bp.route('/login', methods=['POST'])
def post_login():
    request_arguments = post_request_arguments(request)
    email = request_arguments['email']
    password = request_arguments['password']

    if not email or not password:
        return "Bad request", 400

    user = User.get_by_email_and_password(email, password)
    if user:
        login_user(user)
        if request.content_type == 'application/x-www-form-urlencoded':
            return redirect(url_for('auth.get_profile'))
        return api_response(user.to_dict(), request.content_type)
    return "Invalid email or password", 401

@bp.route('/logout', methods=['POST'])
@login_required
def post_logout():
    logout_user()
    return redirect(url_for('auth.get_login'))

@bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    return render_template('auth/profile.html', user=current_user, establishment_names=Violation.establishment_names())

@bp.route('/profile', methods=['POST'])
@login_required
def post_profile():
    request_arguments = post_request_arguments(request)

    if request.content_type == 'application/x-www-form-urlencoded':
        return redirect(url_for('auth.get_profile'))
    return api_response(current_user.to_dict(), request.content_type)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    match = re.match(pattern, email)
    return match is not None
