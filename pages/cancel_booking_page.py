from notifications.booking_notifications import booking_cancelled, booking_pending_cancelled
from flask import session, redirect, url_for, request, jsonify
from app import db
from datetime import datetime, date
from models import Users, Bookings, TrainingSessions

def cancel_booking(booking_id):

    booking = Bookings.query.filter_by(BookingId=booking_id).first()

    user = booking.user
    training_session = booking.session
    trainer = training_session.trainer

    was_pending = booking.Status == "Pending Approval"

    if training_session.Booked > 0:
        training_session.Booked -= 1
    booking.CancelledAt = date.today()

    if not booking or booking.UserId != session.get('user_id'):
        return jsonify({"status": "error", "message": "Booking not found."}), 404
    
    reason = request.form.get('reason', '').strip()

    if not reason:
        return jsonify({
            "status": "error",
            "message": "Please provide a reason for your cancellation."
        }), 400

    booking.Status = "Cancelled"
    booking.CancelReason = reason

    db.session.delete(booking.attendance)
    db.session.commit()

    if was_pending:
        booking_pending_cancelled(user, training_session)
    else:
        booking_cancelled(user, training_session, trainer)

    return jsonify({
        "status": "success",
        "message": f"Your booking for {booking.session.Title} has been cancelled"
    }), 200