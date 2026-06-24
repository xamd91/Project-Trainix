from flask import request, render_template, session, redirect, url_for, jsonify
from models import Users, Departments, TrainingSessions, TrainingCourses
from app import db

def create_department():

    if request.method == "POST":

        name = request.form.get('name', '').strip()
        manager_id = int(request.form.get('manager'))

        if not name or not manager_id:
            return jsonify({
                "status": "error",
                "message": "All fields are required."
            }), 400
        
        if len(name) > 100 or len(name) < 3:
            return jsonify({
                "status": "error",
                "message": "Department name must be between 3-100 characters."
            }), 400

        if Departments.query.filter_by(DepartmentName=name.title()).first():
            return jsonify({
                "status": "error",
                "message": "Department already exists."
            }), 400
        
        valid_manager = (
            Users.query
            .filter(
                Users.UserId == manager_id,
                Users.Role == "Manager"
            )
            .first()
            is not None
        )

        if not valid_manager:
            return jsonify({
                "status": "error",
                "message": "Manager does not exist."
            }), 400

        department = Departments(
            DepartmentName=name.title(),
            ManagerId=manager_id
        )

        db.session.add(department)
        db.session.commit()

        created_department = Departments.query.filter_by(DepartmentName=name).first()

        if create_department:
            return jsonify({
                 "status": "success",
                 "message": f"{name} department created successfully!"
            }), 201
        else:
            return jsonify({
                "status": "error",
                "message": "Something went wrong while creating the department."
            }), 400

    return redirect(url_for('admin_dashboard', tab='department_management'))