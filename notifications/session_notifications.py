from .email_service import send_email
from models import Bookings

def session_cancelled(session):

    approved_bookings = (
        Bookings.query
        .filter_by(
            SessionId=session.SessionId,
            Status="Approved"
        )
        .all()
    )

    for booking in approved_bookings:

        attendee = booking.user

        send_email(
            to=attendee.Email,
            subject=f"Session Cancelled - {session.Title}",
            template="session_cancelled",
            context={
                "user": attendee,
                "session": session
            }
        )

def session_updated(session, changes):

    approved_bookings = (
        Bookings.query
        .filter_by(
            SessionId=session.SessionId,
            Status="Approved"
        )
        .all()
    )

    for booking in approved_bookings:

        attendee = booking.user

        send_email(
            to=attendee.Email,
            subject=f"Session Updated - {session.Title}",
            template="session_updated",
            context={
                "user": attendee,
                "session": session,
                "changes": changes
            }
        )