from flask import render_template, session, redirect, url_for
from models import Users, TrainingSessions

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('manager_dashboard.html', user=Users.query.filter_by(UserId = session['user_id']), sessions=TrainingSessions.query.all())
    