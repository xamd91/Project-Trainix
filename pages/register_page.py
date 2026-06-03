import re
from flask import request, render_template, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users
from app import db

def page():
    
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == "POST":

        firstname = request.form.get('firstname', '').strip()
        lastname = request.form.get('lastname', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm-password', '').strip()

        if not all([firstname, lastname, email, phone, password, confirm_password]):
            return jsonify({
                "status": "error",
                "message": "All fields are required."
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
        

        if Users.query.filter_by(Phone=phone).first():
            return jsonify({
                "status": "error",
                "message": "Phone number already registered."
            }), 400

        if len(password) < 8:
            return jsonify({
                "status": "error",
                "message": "Password must be at least 8 characters."
            }), 400

        if not any(ch.isupper() for ch in password):
            return jsonify({
                "status": "error",
                "message": "Password must contain at least 1 uppercase letter."
            }), 400

        if not any(ch.islower() for ch in password):
            return jsonify({
                "status": "error",
                "message": "Password must contain at least 1 lowercase letter."
            }), 400

        if not any(ch.isdigit() for ch in password):
            return jsonify({
                "status": "error",
                "message": "Password must contain at least 1 number."
            }), 400

        if password.isalnum():
            return jsonify({
                "status": "error",
                "message": "Password must contain at least 1 special character."
            }), 400

        if password != confirm_password:
            return jsonify({
                "status": "error",
                "message": "Passwords do not match."
            }), 400

        user = Users(
            FirstName=firstname.capitalize(),
            LastName=lastname.capitalize(),
            Phone=phone,
            Email=email,
            Password=generate_password_hash(password),
            Role="Learner"
        )

        db.session.add(user)
        db.session.commit()

        created_user = Users.query.filter_by(Email=request.form['email']).first()

        if created_user:
            return jsonify({
                 "status": "success",
                 "message": f"Account for {created_user.FirstName} created successfully!"
            }), 201
        else:
            return jsonify({
                "status": "error",
                "message": "Something went wrong while creating the account."
            }), 400


    return render_template("register.html")