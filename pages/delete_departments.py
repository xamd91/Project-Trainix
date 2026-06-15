from flask import render_template, session, redirect, url_for, request
from models import Departments
from sqlalchemy import or_
from app import db

def delete_department(department_id):

    department = Departments.query.get(department_id)

    db.session.delete(department)
    db.session.commit()
    return redirect(url_for('admin_dashboard', tab='department_management'))