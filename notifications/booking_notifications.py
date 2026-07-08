from .email_service import send_email
from models import Users, Notifications
from app import db
from datetime import datetime, UTC
from zoneinfo import ZoneInfo


def create_in_app_notification(user, message, notification_type="Booking", booking=None):
    # creates a notification row for a user. Powers nav badge count and notifications tab.
    notification = Notifications(
        UserId=user.UserId,
        Message=message,
        NotificationType=notification_type,
        IsRead=False,
        CreatedAt=datetime.now(UTC),
        RelatedBookingId=booking.BookingId if booking else None
    )
    notification.CreatedAt.astimezone(ZoneInfo("Europe/London"))
    db.session.add(notification)
    db.session.commit()

def booking_requested(user, session):

    manager = Users.query.filter_by(UserId=user.ManagerId).first()
                                                    
    send_email(
        to=user.Email,
        subject="Booking request submitted",
        template="booking_requested_user",
        context={
            "user": user,
            "session": session
        }
    )

    if manager:
        send_email(
            to=manager.Email,
            subject="Approval required: new booking request",
            template="booking_requested_manager",
            context={
                "user": user,
                "session": session,
                "manager": manager
            }
        )
    
    create_in_app_notification(
        user=user,
        message=f'Your booking request for {session.Title} has been submitted and is awaiting approval.',
        notification_type="Booking"
    )
    # booking states below are unchanged, can extend each one the same way (call create_in_app_notification) whenever you want those to show up in-app.

def booking_approved(user, session, type):

    trainer = session.trainer

    send_email(
        to=user.Email,
        subject="Booking request approved",
        template="booking_approved",
        context={
            "user": user,
            "session": session,
            "type": type,
            "trainer": trainer
        }
    )

    if type == "assigned":
        message = f'You have been added to "{session.Title}".'
    else:
        message = f'Your booking for "{session.Title}" has been approved.'

    create_in_app_notification(
        user=user,
        message=f'Your booking request for {session.Title} has been approved.',
        notification_type="Approval"
    )

def booking_rejected(user, session):

    send_email(
        to=user.Email,
        subject="Booking request rejected",
        template="booking_rejected",
        context={
            "user": user,
            "session": session
        }
    )

    create_in_app_notification(
        user=user,
        message=f'Your booking request for {session.Title} was not approved.',
        notification_type="Approval"
    )

def booking_pending_cancelled(user, session):

    manager = Users.query.filter_by(UserId=user.ManagerId).first()

    if manager:
        send_email(
            to=manager.Email,
            subject="Booking request withdrawn",
            template="pending_booking_cancelled",
            context={
                "user": user,
                "session": session,
                "manager": manager
            }
        )

def booking_cancelled(user, session, trainer):

    send_email(
        to=trainer.Email,
        subject="Booking cancelled",
        template="booking_cancelled_trainer",
        context={
            "user": user,
            "session": session,
            "trainer": trainer
        }
    )

    manager = Users.query.filter_by(UserId=user.ManagerId).first()

    if manager:
        send_email(
            to=manager.Email,
            subject="Booking cancelled",
            template="booking_cancelled_manager",
            context={
                "user": user,
                "session": session,
                "manager": manager
            }
        )
    
    create_in_app_notification(
        user=manager,
        message=f'{user.FirstName} {user.LastName} has cancelled their booking for "{session.Title}".',
        notification_type="Cancellation"
    )