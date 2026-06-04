from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingCourses, Bookings

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    tab = request.args.get('tab', 'bookings')
    subTab = request.args.get('subTab', 'account-details')
    bookings = Bookings.query.filter_by(UserId=session['user_id']).all()
    user_id = session.get('user_id')
    user = Users.query.filter_by(UserId=user_id).first()
    business_area = user.BusinessArea
    manager = Users.query.filter_by(Role='Manager', BusinessArea=business_area).first()
    # trainer = TrainingSessions.query.filter_by(Role='Trainer', BusinessArea=business_area).first()
    return render_template('account.html', user=user, tab=tab, subTab=subTab, bookings=bookings, manager=manager)
    