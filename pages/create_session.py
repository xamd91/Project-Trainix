from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments
from sqlalchemy import or_
from app import db

def create_session():

    training_sessions = TrainingSessions(
        Title = request.form['createSessionTitle'],
        TrainerId = request.form['createSessionTrainer'],
        DepartmentId = request.form['createSessionDepartment']
    )

    db.session.add(training_sessions)
    db.session.commit()
    return redirect(url_for('admin_dashboard', tab='session_management'))