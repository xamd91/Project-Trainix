from flask import session, redirect, url_for, request, jsonify
from app import db
from datetime import datetime
from models import Users, Bookings, TrainingSessions

def cancel_booking(booking_id):

    booking = Bookings.query.filter_by(BookingId=booking_id).first()

    booking.Status = "Cancelled"
    
    db.session.commit()

    return redirect(url_for("account"))