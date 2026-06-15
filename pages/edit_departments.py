from flask import render_template, redirect, url_for, request
from models import Departments
from app import db

def edit_sessions(session_id):

    departments = Departments.query.get(session_id)

    departments.DepartmentName = request.form['department_name']
    departments.ManagerId = request.form['manager']

    db.session.commit()

    return redirect(url_for('admin_dashboard', tab='department_management'))