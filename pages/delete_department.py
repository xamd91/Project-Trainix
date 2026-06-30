from flask import render_template, session, redirect, url_for, jsonify
from models import Departments
from sqlalchemy import or_
from app import db

def delete_department(department_id):

    department = Departments.query.get(department_id)

    users = department.users 

    if users:
        return jsonify({
            "status": "warning",
            "message": f"The {department.DepartmentName} department currently has at least one user assigned to it. Please change the user's department before proceeding."
        }),400
    
    courses = department.courses

    if courses:
        return jsonify({
            "status": "warning",
            "message": f"The {department.DepartmentName} department currently has at least one course assigned to it. Please change the course's department before proceeding."
        }),400
    
    # training_sessions = 



    db.session.delete(department)
    db.session.commit()
    return redirect(url_for('admin_dashboard', tab='department_management'))