import re
from flask import request, session, redirect, url_for, jsonify
from werkzeug.security import check_password_hash
from models import Users
from app import db

def update_profile():

    user_id = session['user_id']

    user = Users.query.filter_by(UserId=user_id).first()

    if request.method == "POST":

        firstname = (request.form.get('firstname') or '').strip()
        lastname = (request.form.get('lastname') or '').strip()
        email = (request.form.get('email') or '').strip()
        phone = (request.form.get('phone') or '').strip()

        if not all([firstname, lastname, email, phone]):
            return jsonify({
                "status": "error",
                "message": "All fields are required."
            }), 400
        
        if firstname == user.FirstName and lastname == user.LastName and email == user.Email and phone == user.Phone:
            return jsonify({
                "status": "warning",
                "message": "No changes detected."
            }), 400
        
        if not firstname.isalpha() or not lastname.isalpha():
            return jsonify({
                "status": "error",
                "message": "First and last names must contain only alphabets."
            }), 400

        if len(firstname) > 45 or len(lastname) > 45:
            return jsonify({
                "status": "error",
                "message": "First and last names must be under 45 characters."
            }),400

        if len(email) > 60:
            return jsonify({
                "status": "error",
                "message": "Email must be under 60 characters."
            }),400

        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            return jsonify({
                "status": "error",
                "message": "Invalid email format."
            }), 400
        
        if email != user.Email:
            if Users.query.filter_by(Email=email).first():
                return jsonify({
                    "status": "error",
                    "message": "Email already exists."
                }), 400
            
        if not phone.isdigit():
            return jsonify({
                "status": "error",
                "message": "Phone number must be digits."
            }), 400

        if len(phone) > 11:
            return jsonify({
                "status": "error",
                "message": "Phone number must not be above 11 digits."
            }), 400
        
        if phone != user.Phone:
            if Users.query.filter_by(Phone=phone).first():
                return jsonify({
                    "status": "error",
                    "message": "Phone number already registered."
                }), 400
            
        user.FirstName = firstname
        user.LastName = lastname
        user.Email = email
        user.Phone = phone

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Profile updated successfully!"
        }), 200
    
    return redirect(url_for("account"))