from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments
from sqlalchemy import or_
from app import db

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # if session['role'] != "trainer":
    #      return redirect(url_for('login'))

    user = Users.query.filter_by(UserId=session['user_id']).first()
    
    return render_template(
        'attendance_management.html', 
        user=user
        )