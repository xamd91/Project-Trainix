from flask import render_template, session, redirect, url_for, jsonify
from models import Users, TrainingSessions, Bookings, Departments
from sqlalchemy import or_
from app import db

def delete_user(user_id):

    user = Users.query.get(user_id)

    if user.Role == 'Manager':

        department = user.department

        if department:

            return jsonify({
                "status": "warning",
                "message": f"This user is currently the manager of {user.department.DepartmentName}. Please change this department's manager before proceeding."
            }),400
        
    elif user.Role == 'Trainer' or user.TrainerPerms == 'Yes':
        
        trianing_sessions = user.training_sessions

        if trianing_sessions:

            return jsonify({
                "status": "warning",
                "message": f"This user is currently assigned as the trainer for at least 1 session. Please change the assigned session's trainer before proceeding."
            }),400


    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User successfully deleted!"
    }),200

    return redirect(url_for('admin_dashboard', tab='user_management'))