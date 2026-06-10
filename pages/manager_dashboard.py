from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Attendance
from sqlalchemy import or_
from datetime import datetime
from app import db

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    
    if session['role'] != "manager":
        return redirect(url_for('login'))
    
    manager = Users.query.get(user_id)

    department = manager.department 

    department_users = department.users if department else []

    team_members = manager.subordinates


    pending_approvals = (
        Bookings.query
        .join(Bookings.user)
        .join(Bookings.session)
        .join(TrainingSessions.course)
        .filter(
            or_(
                Users.ManagerId == manager.UserId,
                Users.DepartmentId == manager.DepartmentId
            ),
            Bookings.Status == "Pending Approval"
        )
        .all()
    )

    past_approvals = (
        Bookings.query
        .join(Bookings.user)
        .join(Bookings.session)
        .join(TrainingSessions.course)
        .filter(
            or_(
                Users.ManagerId == manager.UserId,
                Users.DepartmentId == manager.DepartmentId
            ),
            Bookings.Status.in_(['Approved', 'Rejected', 'Cancelled'])
        )
        .all()
    )

    # sessions = TrainingSessions.query.all()
    if request.method == 'POST':

        booking_id = request.form.get('booking_id')
        action = request.form.get('action')
        
        booking = Bookings.query.get(booking_id)

        if booking:
            if action == 'approve':
                booking.Status = 'Approved'
                booking.ManagerApproval = "Yes"
                booking.DecidedOn = datetime.utcnow()
                booking.session.Booked += 1
        
                if not booking.attendance:

                    attendance = Attendance(
                        BookingId=booking.BookingId,
                        UserId=booking.UserId,
                        AttendanceStatus="N/A"
                    )
                    db.session.add(attendance)

# training_session.Booked += 1

            elif action == 'reject':
                booking.Status = 'Rejected'
                booking.ManagerApproval = "No"
                booking.DecidedOn = datetime.utcnow()

            db.session.commit()

            return redirect(url_for('manager_dashboard'))
        
    approved = (
        Bookings.query
        .join(Bookings.user)
        .join(Bookings.session)
        .join(TrainingSessions.course)
        .filter(
            or_(
                Users.ManagerId == manager.UserId,
                Users.DepartmentId == manager.DepartmentId
            ),
            Bookings.Status == "Approved"
        )
        .count()
    )

    return render_template(
        'manager_dashboard.html',
        manager=manager,
        department=department,
        department_users=department_users,
        team_members=team_members,
        pending_approvals=pending_approvals,
        past_approvals=past_approvals,
        approved = approved
    )