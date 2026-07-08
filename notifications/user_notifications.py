from.email_service import send_email
from models import Users
from notifications.booking_notifications import create_in_app_notification

def attendance_marked(user, session, status):

    send_email(
        to=user.Email,
        subject=f"Attendance Update - {session.Title}",
        template="attendance_user",
        context={
            "user": user,
            "session": session,
            "status": status.lower()
        }
    )

    create_in_app_notification(
        user=user,
        message=f'You were marked "{status}" for "{session.Title}".',
        notification_type="System"
    )
    
    manager = Users.query.filter_by(UserId=user.ManagerId).first()

    if manager:

        send_email(
            to=manager.Email,
            subject=f"Attendance Update - {user.FirstName}",
            template="attendance_manager",
            context={
                "user": user,
                "manager": manager,
                "session": session,
                "status": status.lower()
            }
        )

        create_in_app_notification(
            user=manager,
            message=f'Your team member "{user.FirstName} {user.LastName}" was marked "{status}" for "{session.Title}".',
            notification_type="System"
        )