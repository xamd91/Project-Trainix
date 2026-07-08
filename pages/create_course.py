from flask import request, render_template, session, redirect, url_for, jsonify
from models import Users, Departments, TrainingSessions, TrainingCourses
from app import db

def create_course():

    if request.method == "POST":

        coursename = request.form.get('coursename')
        description = request.form.get('description')
        department_id = int(request.form.get('department'))

        if not all ([coursename, description, department_id]):
            print(coursename, description, department_id)
            return jsonify({
                "status": "error",
                "message": "Please fill in all mandatory fields."
            }), 400

        if len(coursename) > 100 or len(coursename) < 3:
            return jsonify({
                "status": "error",
                "message": "Course name must be between 3-100 characters."
            }), 400

        if TrainingCourses.query.filter_by(CourseName=coursename).first():
            return jsonify({
                "status": "error",
                "message": "Course name already exists."
            }), 400
        
        valid_department = (
            Departments.query
            .filter(
                TrainingCourses.DepartmentId == department_id,
            )
            .first()
            is not None
        )

        if not valid_department:
            return jsonify({
                "status": "error",
                "message": "Manager does not exist."
            }), 400

        course = TrainingCourses(
            CourseName=coursename,
            Description=description,
            DepartmentId=department_id
        )

        db.session.add(course)
        db.session.commit()

        created_course = TrainingCourses.query.filter_by(CourseName=coursename).first()

        if created_course:
            return jsonify({
                 "status": "success",
                 "message": f"{coursename} course created successfully!"
            }), 201
        else:
            return jsonify({
                "status": "error",
                "message": "Something went wrong while creating the course."
            }), 400

    return redirect(url_for('admin_dashboard', tab='course_management'))