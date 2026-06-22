from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments, TrainingCourses, Attendance
from sqlalchemy import func, or_
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

    bookings = Bookings.query.all()

    normal_sessions = TrainingSessions.query.order_by(TrainingSessions.Date.asc()).all()
        
    total_booked = 0
    total_attended = 0

    for sess in normal_sessions:
        sess.attended_count = 0
        sess.booked_count = 0
        for booking in sess.bookings:
            if booking.Status in ['Approved', 'Completed']:
                total_booked += 1
                sess.booked_count += 1
                if booking.attendance and booking.attendance.AttendanceStatus == "Attended":
                    total_attended += 1
                    sess.attended_count += 1
        sess.attendance_rate = (
            round((sess.attended_count / sess.booked_count) * 100, 1)
            if sess.booked_count > 0
            else 0
        )
    
    if total_booked > 0:
        attendance_rate = round((total_attended / total_booked) * 100, 1)
    else:
        attendance_rate = 0

    total_booked_overview = 0
    total_attended_overview = 0

    completed_sessions = [s for s in normal_sessions if s.Status == "Completed"]

    for sess in completed_sessions:
        for booking in sess.bookings:
            if booking.Status in ['Approved', 'Completed']:
                total_booked_overview += 1

                if booking.attendance and booking.attendance.AttendanceStatus == "Attended":
                    total_attended_overview += 1

    if total_booked_overview > 0:
        overall_attendance_rate = round((total_attended_overview / total_booked_overview) * 100, 1)
    else:
        overall_attendance_rate = 0

    participants = (db.session.query(Attendance.UserId)
                    .filter(Attendance.AttendanceStatus == "Attended")
                    .distinct()
                    .count()
                    )

    return render_template(
        'reports_and_analytics.html',
        admin=admin,
        users=users,
        tab=tab,
        sessions=normal_sessions,
        bookings=bookings,
        attendance_rate=attendance_rate,
        overall_attendance_rate=overall_attendance_rate,
        participants=participants
        )