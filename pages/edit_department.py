from flask import render_template, redirect, url_for, request
from models import Departments
from app import db

def edit_department(department_id):

    departments = Departments.query.get(department_id)

    departments.DepartmentName = request.form['department_name']
    departments.ManagerId = request.form['manager']

    db.session.commit()

    return redirect(url_for('admin_dashboard', tab='department_management'))