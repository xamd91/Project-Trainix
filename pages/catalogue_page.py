from flask import render_template, session
from collections import Counter
from models import Users, TrainingCourses, TrainingSessions
from app import db

def page():

    UserId = session.get('user_id')

    session_list = TrainingSessions.query.all()
    session_count = len(session_list)

    user = Users.query.filter_by(UserId = UserId).first()

    return render_template("training_catalogue.html", session_list=session_list, session_count=session_count, user=user)