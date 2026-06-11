from flask import render_template, redirect, url_for, request
from models import Users
from app import db

def edit_user(user_id):

    user = Users.query.get(user_id)

    user.FirstName = request.form['first_name']
    user.LastName = request.form['last_name']
    user.JobTitle = request.form['job_title']
    user.Role = request.form['role']
    user.DepartmentId = request.form['department']

    db.session.commit()

    return redirect(url_for('admin_dashboard', tab='user_management'))