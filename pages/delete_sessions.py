from flask import render_template, session, redirect, url_for, request
from models import TrainingSessions
from sqlalchemy import or_
from app import db

def delete_sessions(session_id):

    sessions = TrainingSessions.query.get(session_id)

    db.session.delete(sessions)
    db.session.commit()
    return redirect(url_for('admin_dashboard', tab='session_management'))