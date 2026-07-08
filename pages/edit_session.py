from notifications.session_notifications import session_updated
from flask import request, render_template, session, redirect, url_for, jsonify
from models import Users, Departments, TrainingSessions, TrainingCourses
from datetime import datetime, date
from sqlalchemy import or_
from app import db

def edit_session(session_id):

    training_session = TrainingSessions.query.filter_by(SessionId=session_id).first()

    if not training_session:
        return jsonify({"error": "Training session not found."}), 404
    
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
        session_endtime = request.form.get('end_time')
        if session_endtime:
            session_endtime = datetime.strptime(session_endtime, '%H:%M')
        location = request.form.get('location', '').strip()
        capacity = int(request.form.get('capacity'))
        delivery_type = request.form.get('delivery', '').strip()
        description = request.form.get('description', '').strip()
        prerequisites = request.form.get('prerequisites') or None

        if not all ([title, course_id, trainer_id, session_date, session_time,session_endtime, location, capacity, delivery_type, description]):
            return jsonify({
                "status": "error",
                "message": "Please fill in all mandatory fields."
            }), 400
        
        no_change = (title == training_session.Title and course_id == training_session.CourseId 
                     and trainer_id == training_session.TrainerId and session_date == training_session.Date 
                     and session_time == training_session.Time and session_endtime == training_session.EndTime 
                     and location == training_session.Location and capacity == training_session.Capacity 
                     and delivery_type == training_session.DeliveryType and description == training_session.Description 
                     and prerequisites == training_session.prerequisites)

        if no_change:
            return jsonify({
                "status": "warning",
                "message": "No changes detected."
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
        
        if capacity < 1:
            return jsonify({
                "status": "error",
                "message": "Capacity cannot be lower than 1."
            }), 400
        
        if capacity > 100:
            return jsonify({
                "status": "error",
                "message": "Capacity cannot exceed 100."
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
        
        
        changes = {}

        if training_session.Title != title:
            changes["Title"] = {
                "old": training_session.Title,
                "new": title
            }

        if training_session.TrainerId != trainer_id:
            trainer = training_session.TrainerId
            old_trainer = Users.query.get(trainer)
            new_trainer = Users.query.get(trainer_id)
            changes["Trainer"] = {
                "old": f"{old_trainer.FirstName} {old_trainer.LastName}",
                "new": f"{new_trainer.FirstName} {new_trainer.LastName}"
            }

        if training_session.Date != session_date:
            changes["Date"] = {
                "old": training_session.Date.strftime('%d %B %Y'),
                "new": session_date.strftime('%d %B %Y')
            }

        if training_session.Time.strftime('%I:%M %p') != session_time.strftime('%I:%M %p'):
            changes["Time"] = {
                "old": training_session.Time.strftime('%I:%M %p'),
                "new": session_time.strftime('%I:%M %p')
            }

        if training_session.EndTime.strftime('%I:%M %p') != session_endtime.strftime('%I:%M %p'):
            changes["EndTime"] = {
                "old": training_session.EndTime.strftime('%I:%M %p'),
                "new": session_endtime.strftime('%I:%M %p')
            }

        if training_session.Location != location:
            changes["Location"] = {
                "old": training_session.Location,
                "new": location
            }

        print(changes)
        
        training_session.CourseId = course_id
        training_session.TrainerId = trainer_id
        training_session.Title = title.title()
        training_session.Date = session_date
        training_session.Time = session_time
        training_session.EndTime = session_endtime
        training_session.Location = location
        training_session.Capacity = capacity
        training_session.DeliveryType = delivery_type
        training_session.Description = description
        training_session.Prerequisites = prerequisites

        db.session.commit()

        if changes:
            session_updated(training_session, changes)

        return jsonify({
            "status": "success",
            "message": "Session details updated successfully!"
        }), 200

    return redirect(url_for('admin_dashboard', tab='session_management'))