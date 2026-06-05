from flask import render_template, session, redirect, url_for, request
from models import Users, Departments, Bookings

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    tab = request.args.get('tab', 'bookings')
    user_id = session.get('user_id')
    user = Users.query.filter_by(UserId=user_id).first()
    # departments = Departments.query.filter_by(DepartmentName=DepartmentName).first()
    # trainer = TrainingSessions.query.filter_by(Role='Trainer', BusinessArea=business_area).first()
    bookings = Bookings.query.filter_by(UserId=session['user_id']).all()
    return render_template('account.html', user=user, tab=tab, bookings=bookings)
    