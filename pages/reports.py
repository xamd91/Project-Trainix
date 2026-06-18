from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments, TrainingCourses
from sqlalchemy import func
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
    sessions_count = (
        db.session.query(
            TrainingSessions,                          
            func.count(Bookings.BookingId)
        )
        .outerjoin(Bookings, Bookings.SessionId == TrainingSessions.SessionId)
        .group_by(TrainingSessions.SessionId)
        .all()
    )   

    normal_sessions = TrainingSessions.query.order_by(TrainingSessions.Date.asc()).all()

    bookings = Bookings.query.all()
    
    return render_template(
        'reports.html',
        admin=admin,
        users=users,
        tab=tab,
        sessions_count=sessions_count,
        normal_sessions=normal_sessions,
        bookings=bookings
        )