from flask import render_template, session
from collections import Counter
from models import Users, Departments, TrainingSessions, Departments
from app import db

def page():

    UserId = session.get('user_id')

    session_list = TrainingSessions.query.order_by(TrainingSessions.Date.asc()).all()
    session_count = len(session_list)

    for training_session in session_list:
        
        training_session.remaining_slots = (
            training_session.Capacity - training_session.Booked
        )

    user = Users.query.filter_by(UserId = UserId).first()

    departments = Departments.query.all()

    return render_template("training_catalogue.html", session_list=session_list, session_count=session_count, user=user, departments=departments)