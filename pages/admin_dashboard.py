from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments
from sqlalchemy import or_
from app import db

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # if session['role'] != "admin":
    #      return redirect(url_for('login'))
    user_id = session.get('user_id') 

    admin = Users.query.filter_by(UserId=user_id).first()
    users = Users.query.all()
    tab = request.args.get('tab', 'overview')
    active_sessions = TrainingSessions.query.filter(TrainingSessions.Date >= db.func.current_date()).order_by(TrainingSessions.Date).all()
    trainers = Users.query.filter_by(Role='Trainer').all()
    departments = Departments.query.all()

    return render_template(
        'admin_dashboard.html',
        admin=admin,
        users=users,
        tab=tab,
        active_sessions=active_sessions,
        trainers=trainers,
        departments=departments
        )