from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments
from sqlalchemy import or_
from app import db

def create_department():

    departments = Departments(
        DepartmentName = request.form['createDepartmentName'],
        ManagerId = request.form['createDepartmentManager']
    )

    db.session.add(departments)
    db.session.commit()
    return redirect(url_for('admin_dashboard', tab='department_management'))