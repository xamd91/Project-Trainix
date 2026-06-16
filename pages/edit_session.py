from flask import render_template, redirect, url_for, request
from models import TrainingSessions
from app import db

def edit_session(session_id):

    training_sessions = TrainingSessions.query.get(session_id)

    training_sessions.Title = request.form['session_name']
    training_sessions.TrainerId = request.form['trainer']
    training_sessions.DepartmentId = request.form['department']

    db.session.commit()

    return redirect(url_for('admin_dashboard', tab='session_management'))