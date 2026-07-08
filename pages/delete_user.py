from flask import render_template, session, redirect, url_for, jsonify
from models import Users, TrainingSessions, Bookings, Departments
from sqlalchemy import or_
from app import db

def delete_user(user_id):

    user = Users.query.get(user_id)

    was_manager = user.Role == 'Manager' or user.ManagerPerms == 'Yes'

    if was_manager:

        managed_dept = Departments.query.filter_by(ManagerId=user.UserId).all()

        team_members = user.subordinates

        if managed_dept:
            department_names = ", ".join(dept.DepartmentName for dept in managed_dept)

            return jsonify({
                "status": "warning",
                "message": (
                    f"This user is currently the manager of the following departments: "
                    f"{department_names}. Please change the department manager(s) before proceeding."
                )
            }), 400

        elif team_members:
            return jsonify({
                "status": "warning",
                "message": f"This user is currently the manager of at least 1 team member. Please change their manager before proceeding."
            }),400
        
    was_trainer = user.Role == 'Trainer' or user.TrainerPerms == 'Yes'

    if was_trainer:

        training_sessions = user.training_sessions

        if training_sessions:
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