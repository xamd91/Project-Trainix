from notifications.booking_notifications import booking_approved, booking_rejected
from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Attendance
from sqlalchemy import or_
from datetime import datetime, date
from app import db

def page():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    
    if session['role'] != "manager" and not session['manager_perms']:
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
        .order_by(Bookings.BookingDate.desc()).all()
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
        .order_by(Bookings.DecidedOn.desc()).all()
    )

    # sessions = TrainingSessions.query.all()
    if request.method == 'POST':

        booking_id = request.form.get('booking_id')
        action = request.form.get('action')
        
        booking = Bookings.query.get(booking_id)

        if booking:

            user = booking.user
            training_session = booking.session

            if action == 'approve':
                booking.Status = 'Approved'
                booking.ManagerApproval = "Yes"
                booking.DecidedOn = datetime.utcnow()
                booking.ApprovedAt = date.today()
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
                booking.RejectedAt = date.today()

            db.session.commit()

            if action == 'approve':
                booking_approved(user, training_session, type="requested")
            elif action == 'reject':
                booking_rejected(user, training_session)

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

    for member in team_members:
        member_bookings = [
            b for b in member.bookings
            if b.Status == "Approved" and b.attendance
        ]

        member.total_sessions = len(member_bookings)

        member.attend = sum(
            1 for b in member_bookings
            if b.attendance.AttendanceStatus == "Attended"
        )

        member.attendance_rate = (
            round((member.attend / member.total_sessions) * 100)
            if member.total_sessions > 0
            else 0
        )

        member.pending_count = sum(
            1 for b in member.bookings
            if b.Status == "Pending Approval"
        )

    all_member_bookings = [
        b for m in team_members
        for b in m.bookings
        if b.Status == "Approved" and b.attendance
    ]

    total_attended = sum(
        1 for b in all_member_bookings
        if b.attendance.AttendanceStatus == "Attended"
    )

    department_attendance_rate = (
        round((total_attended / len(all_member_bookings)) * 100)
        if all_member_bookings
        else 0
    )

    return render_template(
        'manager_dashboard.html',
        manager=manager,
        department=department,
        department_users=department_users,
        team_members=team_members,
        pending_approvals=pending_approvals,
        past_approvals=past_approvals,
        approved = approved,
        department_attendance_rate = department_attendance_rate
    )