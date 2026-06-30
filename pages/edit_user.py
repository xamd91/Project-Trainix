import re
from flask import request, render_template, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users, Departments
from app import db

def edit_user(user_id):

    user = Users.query.filter_by(UserId=user_id).first()

    if not user:
        return jsonify({"error": "User not found."}), 404
    
    if request.method == "POST":

        firstname = request.form.get('firstname', '').strip()
        lastname = request.form.get('lastname', '').strip()
        email = request.form.get('email', '').strip()
        role = request.form.get('role', '').strip()
        department_id = int(request.form.get('department'))
        trainer_perms = request.form.get('trainer-perms') or None
        job_title = request.form.get('job')

        if not all([firstname, lastname, email, role, department_id, job_title]):
            return jsonify({
                "status": "error",
                "message": "Please fill in all mandatory fields."
            }), 400
        
        no_change = (firstname == user.FirstName and lastname == user.LastName
                     and email == user.Email and role == user.Role and department_id == user.DepartmentId
                     and trainer_perms == user.TrainerPerms and job_title == user.JobTitle)

        if no_change:
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

        valid_roles = ["Learner", "Trainer", "Manager", "Admin"]

        if role not in valid_roles:
            return jsonify({
                "status": "error",
                "message": "Invalid role."
            }), 400
        
        if role == "Trainer":
            trainer_perms = "Yes"

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
    
        user.FirstName = firstname.capitalize()
        user.LastName = lastname.capitalize()
        user.Email = email

        if user.Role == "Manager":

            team_members = user.subordinates

            if team_members:
                return jsonify({
                    "status": "warning",
                    "message": f"This user is currently the manager of {user.department.DepartmentName}. Please change this department's manager before proceeding."
                }),400

        was_trainer = user.Role == 'Trainer' or user.TrainerPerms == 'Yes'

        if was_trainer:

            training_sessions = user.training_sessions

            if training_sessions:
                if role != 'Trainer' and trainer_perms != 'Yes':
                    return jsonify({
                        "status": "warning",
                        "message": f"This user is currently assigned as the trainer for at least 1 session. Please change the assigned session's trainer before proceeding."
                    }),400


        user.Role = role
        user.DepartmentId = department_id
        user.TrainerPerms = trainer_perms
        user.JobTitle = job_title
        

        if dep_manager:
            user.ManagerId = dep_manager.UserId
        
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "User details updated successfully!"
        }), 200

    return redirect(url_for('admin_dashboard', tab='user_management'))