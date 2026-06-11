from flask import session, redirect, url_for, request, jsonify
from app import db
from datetime import datetime
from models import Users, Bookings, TrainingSessions

def complete_session(session_id):

    session = TrainingSessions.query.filter_by(SessionId=session_id).first()

    session.Status = "Completed"

    db.session.commit()

    return redirect(url_for("attendance_management"))