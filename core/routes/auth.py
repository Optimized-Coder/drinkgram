from flask import Blueprint, request, jsonify, render_template, url_for, redirect, flash
from ..extensions import db
from ..models import User
from ..functions import validate_email, validate_username, validate_password

from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__, url_prefix='/auth')

# POST REQUESTS
@auth.route('/register/', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_check = request.form.get('password_check')
        email = request.form.get('email')

        if not validate_username(username):
            return jsonify({'message': 'Username must be between 4 and 20 characters'}), 400
        
        if not validate_password(password):
            return jsonify({'message': 'Password must be between 4 and 20 characters'}), 400
        
        if not validate_email(email):
            return jsonify({'message': 'Email must be valid'}), 400
        
        if password != password_check:
            return jsonify({'message': 'Passwords do not match'}), 400
        
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password, method='sha256'),
            email=email
        )

        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created'}), 201
    
@auth.route('/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not check_password_hash(user.password_hash, password):
            return jsonify({'message': 'Username or password is incorrect'}), 400
        
        login_user(user, remember=True)
        if not current_user.profile_complete:
            flash('Please Update your profile','info')
            return redirect(url_for('auth.edit_profile'))
        
        flash('You are now logged in','success')
        return redirect(url_for('main.index'))
    
@auth.route('/edit_profile/', methods=['POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        location = request.form.get('location')
        about_me = request.form.get('about_me')
        email = request.form.get('email')
        username = request.form.get('username')

        current_user.first_name = f_name
        current_user.last_name = l_name
        current_user.location = location
        current_user.about_me = about_me
        current_user.email = email
        current_user.username = username
        
        db.session.commit()

        flash('Your profile has been updated','success')
        return redirect(url_for('main.profile'))
    
    
# GET
@auth.route('/login/', methods=['GET'])
def login_get():
    return render_template('login.html')

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are now logged out','success')
    return redirect(url_for('main.index'))

@auth.route('/edit_profile/', methods=['GET'])
@login_required
def edit_profile_get():
    return render_template('edit_profile.html')