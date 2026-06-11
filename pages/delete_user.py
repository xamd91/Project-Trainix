from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments
from sqlalchemy import or_
from app import db

def delete_user(user_id):

    user = Users.query.get(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_dashboard', tab='user_management'))