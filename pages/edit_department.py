from flask import request, render_template, session, redirect, url_for, jsonify
from models import Users, Departments, TrainingSessions, TrainingCourses
from sqlalchemy import func
from app import db

def edit_department(department_id):

    department = Departments.query.filter_by(DepartmentId=department_id).first()

    if not department:
        return jsonify({"error": "Department not found."}), 404

    if request.method == "POST":

        name = request.form.get('name', '').strip()
        manager_id = int(request.form.get('manager'))

        if not name or not manager_id:
            return jsonify({
                "status": "error",
                "message": "All fields are required."
            }), 400
        
        if name == department.DepartmentName and manager_id == department.ManagerId:
            return jsonify({
                "status": "warning",
                "message": "No changes detected."
            }), 400

        if len(name) > 100 or len(name) < 3:
            return jsonify({
                "status": "error",
                "message": "Department name must be between 3-100 characters."
            }), 400

        if name.lower() != department.DepartmentName.lower():
            existing = Departments.query.filter(
                    func.lower(Departments.DepartmentName) == name.lower(),
                    Departments.DepartmentId != department.DepartmentId
                ).first()
            if existing:
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
        
        department.DepartmentName = name
        department.ManagerId = manager_id

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Department details updated successfully!"
        }), 200

    return redirect(url_for('admin_dashboard', tab='department_management'))