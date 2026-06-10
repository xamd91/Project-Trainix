from flask import session, redirect, url_for, request, jsonify
from app import db
from datetime import datetime
from models import Users, Bookings, TrainingSessions

def book_session(session_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":

        user_id = session.get('user_id')

        user = Users.query.filter_by(UserId=user_id).first()
        training_session = TrainingSessions.query.filter_by(SessionId=session_id).first()

        existing = Bookings.query.filter_by(UserId=user_id, SessionId=session_id).first()

        if existing:
            return jsonify({
                "status": "error",
                "message": "You have already booked this session."
            }), 400
        
        notes = request.form.get('notes') or None

        booking = Bookings(
            UserId = user_id,
            SessionId = session_id,
            BookingDate = datetime.utcnow(),
            Status = "Pending Approval",
            ManagerApproval = "No",
            Notes = notes
        )

        db.session.add(booking)

        # training_session.Booked += 1

        db.session.commit()

        created_booking = Bookings.query.filter_by(UserId=user_id, SessionId=session_id).first()

        if created_booking:

            return jsonify({
                 "status": "success",
                 "message": "Booking successfully completed!"
            }), 201

