from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments, TrainingCourses, Attendance
from sqlalchemy import or_, func
from datetime import date
from app import db

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # if session['role'] != "admin":
    #      return redirect(url_for('login'))
    user_id = session.get('user_id') 
    session_id = request.args.get('SessionId')

    admin = Users.query.filter_by(UserId=user_id).first()
    users = Users.query.order_by(Users.LastName.asc()).all()
    tab = request.args.get('tab', 'overview')

    upcoming_sessions = (
        TrainingSessions.query.filter(TrainingSessions.Date >= db.func.current_date())
        .order_by(TrainingSessions.Date.asc())
        .limit(5)
    )

    active_sessions = len(
        TrainingSessions.query.filter(TrainingSessions.Date >= db.func.current_date())
        .order_by(TrainingSessions.Date.asc())
        .all()
    )
    
    trainers = (
        Users.query
        .filter(
            or_(
                Users.Role == "Trainer",
                Users.TrainerPerms == "Yes"
            )
        )
        .all()
    )

    managers = Users.query.filter_by(Role='Manager').all()
    departments = Departments.query.order_by(Departments.DepartmentName.asc()).all()
    training_sessions = TrainingSessions.query.order_by(TrainingSessions.Date.desc()).all()
    courses = TrainingCourses.query.all()
    roles = db.session.scalars(db.session.query(Users.Role).distinct()).all()
    
    today = date.today()

    attendance_counts = (
        db.session.query(Attendance.AttendanceStatus, func.count(Attendance.AttendanceId))
        .join(Bookings, Attendance.BookingId == Bookings.BookingId)
        .join(TrainingSessions, Bookings.SessionId == TrainingSessions.SessionId)
        .filter(TrainingSessions.Status == 'Completed')
        .group_by(Attendance.AttendanceStatus)
        .all()
    )

    att_counts = {status: count for status, count in attendance_counts}
    attended = att_counts.get('Attended', 0)
    absent = att_counts.get('Absent', 0)
    marked_total = attended + absent

    overall_attendance_rate = round((attended / marked_total) * 100, 1) if marked_total else 0
    

    return render_template(
        'admin_dashboard.html',
        admin=admin,
        users=users,
        tab=tab,
        upcoming_sessions=upcoming_sessions,
        trainers=trainers,
        managers=managers,
        departments=departments,
        training_sessions=training_sessions,
        active_sessions=active_sessions,
        courses=courses,
        session_id=session_id,
        roles=roles,
        today=today,
        overall_attendance_rate=overall_attendance_rate
        )