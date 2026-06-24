from flask import request, render_template, session, redirect, url_for, jsonify
from models import Users, Departments, TrainingSessions, TrainingCourses
from datetime import datetime, date
from sqlalchemy import or_
from app import db

def create_session():

    if request.method == "POST":

        title = request.form.get('title', '').strip()
        course_id = int(request.form.get('course'))
        trainer_id = int(request.form.get('trainer'))
        session_date = request.form.get('date')
        if session_date:
            session_date = datetime.strptime(session_date, '%Y-%m-%d').date()
        session_time = request.form.get('time')
        if session_time:
            session_time = datetime.strptime(session_time, '%H:%M')
        location = request.form.get('location', '').strip()
        capacity = int(request.form.get('capacity'))
        delivery_type = request.form.get('delivery', '').strip()
        description = request.form.get('description', '').strip()
        prerequisites = request.form.get('prerequisites') or None

        if not all ([title, course_id, trainer_id, session_date, session_time, location, capacity, delivery_type, description]):
            return jsonify({
                "status": "error",
                "message": "Please fill in all mandatory fields."
            }), 400
        
        if len(title) > 200 or len(title) < 3:
            return jsonify({
                "status": "error",
                "message": "Session title must be between 3-200 characters."
            }), 400
        
        if not TrainingCourses.query.filter_by(CourseId=course_id).first():
            return jsonify({
                "status": "error",
                "message": "Course does not exist."
            }), 400
        
        valid_trainer = (
            Users.query
            .filter(
                Users.UserId == trainer_id,
                or_(
                    Users.Role == "Trainer",
                    Users.TrainerPerms == "Yes"
                )
            )
            .first()
            is not None
        )

        if not valid_trainer:
            return jsonify({
                "status": "error",
                "message": "Trainer does not exist."
            }), 400
        
        if session_date < date.today():
            return jsonify({
                "status": "error",
                "message": "Session date cannot be in the past."
            }), 400

        # time?

        if len(location) > 200:
            return jsonify({
                "status": "error",
                "message": "Location must not exceed 200 characters."
            }), 400
        
        if capacity > 1:
            return jsonify({
                "status": "error",
                "message": "Capacity cannot be lower than 1."
            }), 400
        
        valid_delivery_types = ["Face-to-Face", "Online"]

        if delivery_type not in valid_delivery_types:
            return jsonify({
                "status": "error",
                "message": "Invalid delivery type."
            }), 400
        
        if len(description) > 5000 or len(description) < 22:
            return jsonify({
                "status": "error",
                "message": "Description must be between 22-5000 characters."
            }), 400

        if prerequisites is not None and len(prerequisites) > 5000:
            return jsonify({
                "status": "error",
                "message": "Prerequisites are too long."
            }), 400

        training_session = TrainingSessions(
            CourseId=course_id,
            TrainerId=trainer_id,
            Title=title.title(),
            Date=session_date,
            Time=session_time,
            Location=location,
            Capacity=capacity,
            DeliveryType=delivery_type,
            Description=description,
            Prerequisites=prerequisites,
            Booked=0,
            Status="Not completed",
            Marked=0
        )

        db.session.add(training_session)
        db.session.commit()

        return jsonify({
                "status": "success",
                "message": f"Training session - {title} created successfully!"
        }), 201
    
    return redirect(url_for('admin_dashboard', tab='session_management'))