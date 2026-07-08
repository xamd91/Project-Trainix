from flask import render_template, session
from collections import Counter
from sqlalchemy import or_
from models import Users, Departments, TrainingSessions, Departments
from datetime import datetime
from app import db

def page():

    UserId = session.get('user_id')
    user = Users.query.filter_by(UserId = UserId).first() if UserId else None

    all_sessions = (
        TrainingSessions.query
        .filter(
            or_(
                TrainingSessions.Status == "Not completed"
            ),
        )
        .order_by(TrainingSessions.Date.asc()).all()
    )
    
    # if datetime.combine(TrainingSessions.Date, TrainingSessions.Time) > datetime.now():
    #     TrainingSessions.Status = 'Completed'

    session_list = [
        s for s in all_sessions
        if (
            user is None
            or user.Role == "Admin"
            or (s.course and s.course.department and s.course.department.DepartmentName == "General")
            or (s.course and s.course.DepartmentId == user.DepartmentId)
        )
        and datetime.combine(s.Date, s.Time) > datetime.now()
    ]

    #  session_list = [
    #     s for s in all_sessions
    #     if (
    #         user is None
    #         or user.Role == "Admin"
    #         or s.course.department.DepartmentName == "General"
    #         or s.course.DepartmentId == user.DepartmentId
    #     )
    #     and datetime.combine(s.Date, s.Time) > datetime.now()
    # ]

    session_count = len(session_list)

    for training_session in session_list:
        
        training_session.remaining_slots = (
            training_session.Capacity - training_session.Booked
        )
    
    departments = Departments.query.all()

    return render_template(
        "training_catalogue.html",
        session_list=session_list, 
        session_count=session_count, 
        user=user, 
        departments=departments
        )