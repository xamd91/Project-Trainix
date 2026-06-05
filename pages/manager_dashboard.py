from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments
from app import db

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = Users.query.filter_by(UserId=session['user_id']).first()
    sessions = TrainingSessions.query.all()
    if request.method == 'POST':
        booking_id = request.form.get('booking_id')
        action = request.form.get('action')
        booking = Bookings.query.get(booking_id)

        if booking:
            if action == 'approve':
                booking.Status = 'Approved'
                booking.ManagerApproval = "Yes"
            elif action == 'reject':
                booking.Status = 'Rejected'
                booking.ManagerApproval = "No"
            db.session.commit()
        return redirect(url_for('account', tab='bookings'))
    bookings = Bookings.query.join(Users, Bookings.UserId == Users.UserId).filter(Users.DepartmentId == user.DepartmentId).all()
    return render_template('manager_dashboard.html', user=user, sessions=sessions, bookings=bookings)
    