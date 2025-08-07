import re
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from models.user_model import User
from database import users_collection, wallets_collection
from bson.objectid import ObjectId
from extensions import mail  # ⬅️ Initialized in your main app

auth_bp = Blueprint('auth', __name__, template_folder='templates')


def is_valid_password(password):
    return (
        len(password) >= 8 and
        re.search(r'[a-z]', password) and
        re.search(r'[A-Z]', password) and
        re.search(r'\d', password) and
        re.search(r'[\W_]', password)
    )


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')

        if users_collection.find_one({"email": email}):
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.register'))

        if not is_valid_password(password):
            flash('Password must include uppercase, lowercase, number, special character, and be at least 8 characters.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        new_user = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "password": hashed_password,
            "role": "user",  # Default role
          
        }

        user_id = users_collection.insert_one(new_user).inserted_id

        wallets_collection.insert_one({
            "user_id": str(user_id),
            "balance": 0.0
        })

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')

        user_data = users_collection.find_one({
            "$or": [{"email": identifier}, {"phone": identifier}]
        })

        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            flash('Login successful!', 'success')
            if user.role == "admin":
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(request.args.get('next') or url_for('dashboard.dashboard'))

        flash('Invalid credentials', 'danger')

    return render_template('auth/login.html')



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = users_collection.find_one({"email": email})

        if user:
            token = str(uuid.uuid4())
            users_collection.update_one({"_id": user["_id"]}, {"$set": {"reset_token": token}})

            reset_link = url_for('auth.reset_password', token=token, _external=True)

            msg = Message(subject='VTU portal Password Reset Request',
                          sender=current_app.config['MAIL_USERNAME'],
                          recipients=[email])
            msg.body = f"Click the link below to reset your password:\n{reset_link}"
            mail.send(msg)

            flash('Password reset link sent. Check your email.', 'info')
        else:
            flash('No account found with that email.', 'warning')

    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = users_collection.find_one({"reset_token": token})
    if not user:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        if not is_valid_password(new_password):
            flash('Password must include uppercase, lowercase, number, special character, and be at least 8 characters.', 'danger')
            return redirect(request.url)

        hashed = generate_password_hash(new_password)
        users_collection.update_one({"_id": user["_id"]}, {
            "$set": {"password": hashed},
            "$unset": {"reset_token": ""}
        })

        flash('Password reset successful. You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html')
