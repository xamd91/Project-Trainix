from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments
from sqlalchemy import or_
from app import db

def create_user():

    user = Users(
        FirstName=request.form['first_name'],
        LastName=request.form['last_name'],
        JobTitle=request.form['job_title'],
        Role=request.form['role'],
        DepartmentId=int(request.form['department'])
    )

    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin_dashboard', tab='user_management'))