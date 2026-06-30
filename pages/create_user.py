import re
from flask import request, render_template, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users, Departments
from app import db

def create_user():

    if request.method == "POST":
        
        firstname = request.form.get('firstname', '').strip()
        lastname = request.form.get('lastname', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', '').strip()
        department_id = int(request.form.get('department'))
        job_title = request.form.get('job')


        if not all([firstname, lastname, email, password, role, department_id, job_title]):
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

        valid_roles = ["Learner", "Trainer", "Manager", "Admin"]

        if role not in valid_roles:
            return jsonify({
                "status": "error",
                "message": "Invalid role."
            }), 400

        if not Departments.query.filter_by(DepartmentId=department_id).first():
            return jsonify({
                "status": "error",
                "message": "Department does not exist."
            }), 400
        
        if len(job_title) > 100 or len(job_title) < 3:
            return jsonify({
                "status": "error",
                "message": "Job title must be between 3-100 characters."
            }),400
        
        department = Departments.query.filter_by(DepartmentId=department_id).first()
        dep_manager = department.manager

        user = Users(
            FirstName=firstname.capitalize(),
            LastName=lastname.capitalize(),
            Email=email,
            Password=generate_password_hash(password),
            Role=role,
            DepartmentId=department_id,
            JobTitle=job_title.title(),
            ManagerId=dep_manager.UserId if dep_manager else None
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

    return redirect(url_for('admin_dashboard', tab='user_management'))