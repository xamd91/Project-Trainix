from flask import render_template, session, redirect, url_for, request
from models import Users, Departments, Bookings, Attendance
from sqlalchemy import or_

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    tab = request.args.get('tab', 'bookings')
    user_id = session.get('user_id')
    user = Users.query.filter_by(UserId=user_id).first()
    
    # departments = Departments.query.filter_by(DepartmentName=DepartmentName).first()
    # trainer = TrainingSessions.query.filter_by(Role='Trainer', BusinessArea=business_area).first()

    attendance = Attendance.query.filter_by(UserId=session['user_id']).all()
    bookings = Bookings.query.filter_by(UserId=session['user_id']).all()

    # attendance_records = Attendance.query.all()
    
    # user_attendance = Attendance.query.filter_by(UserId=user_id).first()
    # print(user_attendance.booking.session.Title)
    
    manager = Users.query.filter_by(DepartmentId=user.DepartmentId, Role='Manager').first()
    upcoming_bookings = Bookings.query.outerjoin(Bookings.attendance).filter(Bookings.UserId == session['user_id'], Bookings.Status.in_(['Pending Approval', 'Approved' ])).all()
    booking_history = Bookings.query.join(Bookings.attendance).filter(Bookings.UserId == session['user_id'], Attendance.AttendanceStatus.in_(['Attended', 'Absent']), Bookings.Status == 'Completed').all()
    
    
    
    return render_template(
        'account.html', 
        user=user, 
        tab=tab, 
        bookings=bookings,
        manager=manager,
        booking_history=booking_history, 
        upcoming_bookings=upcoming_bookings, 
        attendance=attendance
        )
    