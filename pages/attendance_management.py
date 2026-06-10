from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments
from sqlalchemy import or_
from app import db

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # if session['role'] != "trainer":
    #      return redirect(url_for('login'))
    user_id = session.get('user_id') 

    trainer = Users.query.filter_by(UserId=user_id).first()
    # print(trainer.UserId)
    upcoming_sessions = (
        TrainingSessions.query
        .filter(
            or_(
                TrainingSessions.Status != "Completed",
                TrainingSessions.Status.is_(None)
            ),
            TrainingSessions.TrainerId == user_id
        )
        .all()
    )
    # print(upcoming_sessions)

    for training_session in upcoming_sessions:
        training_session.approved_bookings = [
            booking
            for booking in training_session.bookings
            if booking.Status == "Approved"
        ]
    
    return render_template(
        'attendance_management.html', 
        trainer=trainer,
        upcoming_sessions=upcoming_sessions,
        )