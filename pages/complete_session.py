from flask import session, redirect, url_for, request, jsonify
from app import db
from datetime import datetime
from models import Users, Bookings, TrainingSessions

def complete_session(session_id):

    training_session = TrainingSessions.query.filter_by(
        SessionId=session_id
    ).first()

    approved_bookings = Bookings.query.filter_by(
        SessionId=session_id,
        Status="Approved"
    ).all()

    missing_attendance = any(
        booking.attendance.AttendanceStatus not in ["Attended", "Absent"]
        for booking in approved_bookings
    )

    if missing_attendance:
        return jsonify({
            "status": "error",
            "message": "Attendance must be marked for all attendees before completing the session."
        }), 400

    training_session.Status = "Completed"

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": f"{training_session.Title} has been marked as completed."
    }), 400

    return redirect(url_for("attendance_management"))