from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Attendance
from sqlalchemy import or_

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    tab = request.args.get('tab', 'bookings')

    user_id = session.get('user_id')
    user = Users.query.filter_by(UserId=user_id).first()
    
    attendance = Attendance.query.filter_by(UserId=session['user_id']).all()

    bookings = Bookings.query.filter_by(UserId=session['user_id']).all()

    manager = Users.query.filter_by(DepartmentId=user.DepartmentId, Role='Manager').first()

    upcoming_bookings = (
        Bookings.query
        .join(Bookings.session)
        .filter(
            or_(
                Bookings.Status == "Pending Approval",
                Bookings.Status == "Approved"
            ),
            Bookings.UserId == user_id
        )
        .order_by(TrainingSessions.Date.asc()).all()
    )

    inactive_bookings = (
        Bookings.query
        .join(Bookings.session)
        .filter(
            or_(
                Bookings.Status == "Rejected",
                Bookings.Status == "Cancelled"
            ),
            Bookings.UserId == user_id
        )
        .order_by(TrainingSessions.Date.desc()).all()
    )

    training_history = (
        Bookings.query
        .join(Bookings.session)
        .join(Bookings.attendance)
        .filter(
            Bookings.UserId == user_id,
            Bookings.Status == "Approved",
            TrainingSessions.Status == "Completed"
        )
        .order_by(TrainingSessions.Date.desc()).all()
    )


    # upcoming_bookings = Bookings.query.outerjoin(Bookings.attendance).filter(Bookings.UserId == session['user_id'], Bookings.Status.in_(['Pending Approval', 'Approved' ])).all()
    
    
    
    
    return render_template(
        'account.html', 
        user=user, 
        tab=tab, 
        bookings=bookings, 
        upcoming_bookings=upcoming_bookings,
        inactive_bookings=inactive_bookings,
        training_history=training_history,
        attendance=attendance
        )
    