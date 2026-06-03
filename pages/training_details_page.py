from flask import render_template, session, redirect, url_for
from models import Users, TrainingSessions, TrainingCourses
from app import db

def page(session_id):

    training_session = TrainingSessions.query.get(session_id)

    user_id = session.get('user_id')

    user = Users.query.filter_by(UserId=user_id).first()

    if training_session is None:
        return redirect(url_for('training_catalogue'))
    
    business_area = user.BusinessArea

    manager = Users.query.filter_by(Role='Manager', BusinessArea=business_area).first()

    return render_template("training_details.html", user=user, training_session=training_session, manager=manager)