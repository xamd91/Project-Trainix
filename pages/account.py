from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    tab = request.args.get('tab', 'bookings')
    booking = TrainingSessions.query.filter_by(SessionId=session['user_id']).all()
    user_id = session.get('user_id')
    user = Users.query.filter_by(UserId=user_id).first()
    return render_template('account.html', user=user, tab=tab, booking=booking)
    