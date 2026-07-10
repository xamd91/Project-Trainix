from notifications.session_notifications import session_cancelled
from flask import session, redirect, url_for, request, jsonify
from app import db
from datetime import datetime
from models import Users, Bookings, TrainingSessions

def cancel_session(session_id):

    training_session = TrainingSessions.query.filter_by(
        SessionId=session_id
    ).first()

    training_session.Status = "Cancelled"

    db.session.commit()
    session_cancelled(training_session)

    return redirect(url_for("attendance_management"))