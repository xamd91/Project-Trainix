from flask import request, render_template, session, redirect, url_for, jsonify
from models import Users, Departments, TrainingSessions, TrainingCourses
from sqlalchemy import func
from app import db

def edit_course(course_id):

    course = TrainingCourses.query.filter_by(CourseId=course_id).first()

    if not course:
        return jsonify({"error": "Course not found."}), 404

    if request.method == "POST":

        coursename = request.form.get('coursename')
        description = request.form.get('description')
        department = int(request.form.get('department'))

        if not coursename or not description or not department:
            return jsonify({
                "status": "error",
                "message": "All fields are required."
            }), 400
        
        if coursename == course.CourseName and description == course.Description and department == course.DepartmentId:
            return jsonify({
                "status": "warning",
                "message": "No changes detected."
            }), 400

        if len(coursename) > 100 or len(coursename) < 3:
            return jsonify({
                "status": "error",
                "message": "Department name must be between 3-100 characters."
            }), 400

        if coursename.lower() != course.CourseName.lower():
            existing = TrainingCourses.query.filter(
                    func.lower(course.CourseName) == coursename.lower(),
                    TrainingCourses.CourseId != course.CourseId
                ).first()
            if existing:
                return jsonify({
                    "status": "error",
                    "message": "Course already exists."
                }), 400
        
        valid_department = (
            Departments.query
            .filter(
                course.DepartmentId == department,
            )
            .first()
            is not None
        )

        if not valid_department:
            return jsonify({
                "status": "error",
                "message": "Manager does not exist."
            }), 400

        course.CourseName = coursename
        course.Description = description
        course.DepartmentId = department

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Course details updated successfully!"
        }), 200

    return redirect(url_for('admin_dashboard', tab='course_management'))