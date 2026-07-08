from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments
from sqlalchemy import or_
from datetime import date, datetime
from app import db

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if session['role'] != "trainer" and not session['trainer_perms']:
         return redirect(url_for('login'))
    

    user_id = session.get('user_id') 

    trainer = Users.query.filter_by(UserId=user_id).first()
    # print(trainer.UserId)
    upcoming_sessions = (
        TrainingSessions.query
        .filter(
            or_(
                TrainingSessions.Status == "Not completed",
                TrainingSessions.Status.is_(None)
            ),
            TrainingSessions.TrainerId == user_id
        )
        .order_by(TrainingSessions.Date.asc()).all()
    )
    # print(upcoming_sessions)

    for training_session in upcoming_sessions:
        training_session.approved_bookings = [
            booking
            for booking in training_session.bookings
            if booking.Status == "Approved"
        ]

        session_datetime = datetime.combine(training_session.Date, training_session.Time)
        training_session.has_started = datetime.now() >= session_datetime

    total_upcoming_attendees = sum(
        len(training_session.approved_bookings)
        for training_session in upcoming_sessions
    )
    
    past_sessions = (
        TrainingSessions.query
        .filter(
            or_(
            
                TrainingSessions.Status == "Completed",
                TrainingSessions.Status == "Cancelled"
            ),
            TrainingSessions.TrainerId == user_id
        )
        .order_by(TrainingSessions.Date.desc()).all()
    )   
        
    for training_session in past_sessions:
        training_session.approved_bookings = [
            booking
            for booking in training_session.bookings
            if booking.Status == "Approved"
        ]

        training_session.approved_count = len(training_session.approved_bookings)

        training_session.attended_count = sum(
            1
            for booking in training_session.approved_bookings
            if booking.attendance and booking.attendance.AttendanceStatus == "Attended"
        )

        training_session.absent_count = sum(
            1
            for booking in training_session.approved_bookings
            if booking.attendance and booking.attendance.AttendanceStatus == "Absent"
        )

        training_session.rate = (
            int(training_session.attended_count / training_session.approved_count * 100) 
            if training_session.approved_count > 0 
            else 0
        )

    session_count = len(upcoming_sessions) + len(past_sessions)

    total_attended = sum(
        session.attended_count
        for session in past_sessions
    )

    total_approved = sum(
        session.approved_count
        for session in past_sessions
    )

    average_attendance_rate = (
        round((total_attended / total_approved) * 100, 1)
        if total_approved > 0
        else 0
    )

    today = date.today()

    sessions_today = (
        TrainingSessions.query
        .filter(
            TrainingSessions.TrainerId == user_id,
            TrainingSessions.Date == today,
            TrainingSessions.Status == 'Not completed'
        )
        .all()
    )
    
    users = Users.query.all()

    return render_template(
        'attendance_management.html', 
        trainer=trainer,
        upcoming_sessions=upcoming_sessions,
        past_sessions=past_sessions,
        session_count=session_count,
        sessions_today=sessions_today,
        total_upcoming_attendees=total_upcoming_attendees,
        average_attendance_rate=average_attendance_rate,
        users=users
        )