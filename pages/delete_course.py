from flask import jsonify
from models import TrainingCourses
from app import db


def delete_course(course_id):

    course = TrainingCourses.query.get(course_id)

    if not course:
        return jsonify({
            "status": "error",
            "message": "Course not found."
        }), 404


    sessions = course.sessions

    if sessions:
        session_count = len(sessions)

        db.session.delete(course)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": (
                f"Course successfully deleted along with "
                f"{session_count} assigned training session(s)."
            )
        }), 200


    db.session.delete(course)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Course successfully deleted!"
    }), 200