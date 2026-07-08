from notifications.booking_notifications import booking_approved
from flask import session, redirect, url_for, request, jsonify
from app import db
from datetime import datetime, date
from models import Users, Bookings, TrainingSessions, Attendance

def book_session_attendee(session_id):

    if request.method == "POST":

        user_id = int(request.form.get('user'))

        if not user_id:
            return jsonify({
                "status": "error",
                "message": "A user is required."
            }), 400
        
        if not TrainingSessions.query.filter_by(SessionId=session_id).first():
            return jsonify({
                "status": "error",
                "message": "Training session does not exist."
            }), 400
        
        user = Users.query.filter_by(UserId=user_id).first()
        training_session = TrainingSessions.query.filter_by(SessionId=session_id).first()

        if not user:
            return jsonify({
                "status": "error",
                "message": "User does not exist."
            }), 400
        
        existing_attendee = (
            Bookings.query
            .filter(
                Bookings.SessionId == session_id,
                Bookings.UserId == user_id,
                Bookings.Status == "Approved"
            )
            .first()
        )

        if existing_attendee:
            return jsonify({
                "status": "error",
                "message": f"{user.FirstName} is already an attendee for this session. Please select a different user."
            }), 400
        
        existing_booking = (
            Bookings.query
            .filter(
                Bookings.SessionId == session_id,
                Bookings.UserId == user_id,
                Bookings.Status == "Pending Approval"
            )
            .first()
        )

        if existing_booking:
            return jsonify({
                "status": "error",
                "message": f"A pending booking already exists for {user.FirstName}"
            }), 400
        
        booking = Bookings(
            UserId = user_id,
            SessionId = session_id,
            BookingDate = date.today(),
            Status = "Approved",
            ManagerApproval = "Yes",
            Notes = None,
            DecidedOn = datetime.now(),
            ApprovedAt = date.today()
        )

        db.session.add(booking)
        db.session.flush()

        attendance = Attendance(
            BookingId = booking.BookingId,
            UserId = booking.UserId,
            AttendanceStatus = "N/A"
        )

        booking.session.Booked += 1

        db.session.add(attendance)
        db.session.commit()

        booking_approved(user, training_session, type="assigned")

        return jsonify({
            "status": "success",
            "message": f"Booking successfully placed for {user.FirstName}"
        }), 201