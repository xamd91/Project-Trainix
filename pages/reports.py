from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments, TrainingCourses, Attendance
from sqlalchemy import func, or_, extract, case, distinct
from app import db
from datetime import date
from collections import defaultdict

MONTH_LABELS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

FUNNEL_COLORS = {
    'Completed': '#10b981',
    'Approved': '#00B0C2',
    'Pending Approval': '#F99D20',
    'Cancelled': '#f97316',
    'Rejected': '#ef4444',
}

def page():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    
    if session['role'] != "admin" and not session['admin_perms']:
        return redirect(url_for('login'))

    # ── STAT CARDS ────────────────────────────────────────────────────────
    total_sessions = (
        db.session.query(func.count(TrainingSessions.SessionId))
        .filter(TrainingSessions.Status == "Completed")
        .scalar()
    ) or 0
    
    total_bookings = db.session.query(func.count(Bookings.BookingId)).scalar() or 0

    today = date.today()
 
    upcoming_bookings = (
        db.session.query(func.count(Bookings.BookingId))
        .join(
            TrainingSessions,
            Bookings.SessionId == TrainingSessions.SessionId
        )
        .filter(
            TrainingSessions.Date > today,
            or_(
                Bookings.Status == 'Approved',
                Bookings.Status == 'Pending Approval'
            ),
            Bookings.CompletedAt.is_(None)
        )
        .scalar()
    ) or 0

    # Attendance rate — Attended vs (Attended + Absent), completed sessions only
    attendance_counts = (
        db.session.query(Attendance.AttendanceStatus, func.count(Attendance.AttendanceId))
        .join(Bookings, Attendance.BookingId == Bookings.BookingId)
        .join(TrainingSessions, Bookings.SessionId == TrainingSessions.SessionId)
        .filter(TrainingSessions.Status == 'Completed')
        .group_by(Attendance.AttendanceStatus)
        .all()
    )

    att_counts = {status: count for status, count in attendance_counts}
    attended = att_counts.get('Attended', 0)
    absent = att_counts.get('Absent', 0)
    marked_total = attended + absent

    overall_attendance_rate = round((attended / marked_total) * 100, 1) if marked_total else 0
    overall_no_show_rate = round((absent / marked_total) * 100, 1) if marked_total else 0

    participants = attended

    # Booking completion rate — Completed / all decided (non-pending) bookings
    status_counts = (
        db.session.query(Bookings.Status, func.count(Bookings.BookingId))
        .group_by(Bookings.Status)
        .all()
    )

    b_counts = {status: count for status, count in status_counts}
    
    completed = (
        db.session.query(func.count(Bookings.BookingId))
        .filter(
            Bookings.CompletedAt.isnot(None),
            Bookings.Status == 'Approved'
        )
        .scalar()
    ) or 0

    pending = b_counts.get('Pending Approval', 0)
    approved = b_counts.get('Approved', 0)
    rejected = b_counts.get('Rejected', 0)
    cancelled = b_counts.get('Cancelled', 0)
    
    decided_total = sum(v for k, v in b_counts.items() if k != 'Pending Approval')
    completion_rate = round((completed / decided_total) * 100, 1) if decided_total else 0

    # ── CHART: SESSIONS BY MONTH ─────────────────────────────────────────
    month_rows = (
        db.session.query(
            extract('month', TrainingSessions.Date).label('month'),
            func.count(TrainingSessions.SessionId)
        )
        .group_by('month')
        .order_by('month')
        .all()
    )
    month_counts = {int(m): c for m, c in month_rows}
    sessions_by_month = {
        'labels': [MONTH_LABELS[i - 1] for i in sorted(month_counts)],
        'data': [month_counts[i] for i in sorted(month_counts)],
    }

    # ── CHART: SESSIONS BY DEPARTMENT ─────────────────────────────────────
    dept_session_rows = (
        db.session.query(Departments.DepartmentName, func.count(TrainingSessions.SessionId))
        .join(TrainingCourses, TrainingCourses.DepartmentId == Departments.DepartmentId)
        .join(TrainingSessions, TrainingSessions.CourseId == TrainingCourses.CourseId)
        .group_by(Departments.DepartmentName)
        .all()
    )
    sessions_by_dept = {
        'labels': [r[0] for r in dept_session_rows],
        'data': [r[1] for r in dept_session_rows],
    }

    # ── CHART: ATTENDANCE TREND (line, % per month) ───────────────────────
    trend_rows = (
        db.session.query(
            extract('month', TrainingSessions.Date).label('month'),
            Attendance.AttendanceStatus,
            func.count(Attendance.AttendanceId)
        )
        .join(Bookings, Attendance.BookingId == Bookings.BookingId)
        .join(TrainingSessions, Bookings.SessionId == TrainingSessions.SessionId)
        .group_by('month', Attendance.AttendanceStatus)
        .order_by('month')
        .all()
    )
    trend_monthly = defaultdict(lambda: {'Attended': 0, 'Absent': 0})
    for month, status, count in trend_rows:
        if status in ('Attended', 'Absent'):
            trend_monthly[int(month)][status] = count

    trend_months_sorted = sorted(trend_monthly.keys())
    attendance_trend = {
        'labels': [MONTH_LABELS[m - 1] for m in trend_months_sorted],
        'data': [
            round((trend_monthly[m]['Attended'] /
                   (trend_monthly[m]['Attended'] + trend_monthly[m]['Absent'])) * 100, 1)
            if (trend_monthly[m]['Attended'] + trend_monthly[m]['Absent']) else 0
            for m in trend_months_sorted
        ],
    }

    # ── CHART: DELIVERY TYPE SPLIT ─────────────────────────────────────────
    delivery_rows = (
        db.session.query(TrainingSessions.DeliveryType, func.count(TrainingSessions.SessionId))
        .group_by(TrainingSessions.DeliveryType)
        .all()
    )
    delivery_counts = {dtype: count for dtype, count in delivery_rows}
    delivery_split = {
        'labels': ['Face-to-Face', 'Online'],
        'data': [delivery_counts.get('Face-to-Face', 0), delivery_counts.get('Online', 0)],
    }

    # ── CHART: ATTENDANCE STACK BY MONTH ───────────────────────────────────
    stack_rows = (
        db.session.query(
            extract('month', TrainingSessions.Date).label('month'),
            Attendance.AttendanceStatus,
            func.count(Attendance.AttendanceId)
        )
        .join(Bookings, Attendance.BookingId == Bookings.BookingId)
        .join(TrainingSessions, Bookings.SessionId == TrainingSessions.SessionId)
        .group_by('month', Attendance.AttendanceStatus)
        .order_by('month')
        .all()
    )
    stack_monthly = defaultdict(lambda: {'Attended': 0, 'Absent': 0, 'N/A': 0})
    for month, status, count in stack_rows:
        stack_monthly[int(month)][status] = count

    stack_months_sorted = sorted(stack_monthly.keys())
    attendance_stack = {
        'labels': [MONTH_LABELS[m - 1] for m in stack_months_sorted],
        'attended': [stack_monthly[m]['Attended'] for m in stack_months_sorted],
        'absent': [stack_monthly[m]['Absent'] for m in stack_months_sorted],
        'na': [stack_monthly[m]['N/A'] for m in stack_months_sorted],
    }


    pie_rows = (
        db.session.query(Attendance.AttendanceStatus, func.count(Attendance.AttendanceId))
        .join(Attendance.booking)
        .join(Bookings.session)
        .filter(TrainingSessions.Status == 'Completed')
        .group_by(Attendance.AttendanceStatus)
        .all()
    )
    
    pie_counts = {status: count for status, count in pie_rows}
    
    attendance_pie = {
        'attended': pie_counts.get('Attended', 0),
        'absent': pie_counts.get('Absent', 0),
    }

    funnel_data = {
        'Completed': completed,
        'Approved': approved,
        'Pending Approval': pending,
        'Cancelled': cancelled,
        'Rejected': rejected,
    }

    booking_funnel = [
        {'label': label, 'count': funnel_data.get(label, 0), 'color': color}
        for label, color in FUNNEL_COLORS.items()
    ]

    approved_rows = (
        db.session.query(
            extract('month', Bookings.ApprovedAt),
            func.count(Bookings.BookingId)
        )
        .filter(Bookings.ApprovedAt.isnot(None))
        .group_by(extract('month', Bookings.ApprovedAt))
        .all()
    )

    cancelled_rows = (
        db.session.query(
            extract('month', Bookings.CancelledAt),
            func.count(Bookings.BookingId)
        )
        .filter(Bookings.CancelledAt.isnot(None))
        .group_by(extract('month', Bookings.CancelledAt))
        .all()
    )

    completed_rows = (
        db.session.query(
            extract('month', Bookings.CompletedAt),
            func.count(Bookings.BookingId)
        )
        .filter(Bookings.CompletedAt.isnot(None))
        .group_by(extract('month', Bookings.CompletedAt))
        .all()
    )

    rejected_rows = (
        db.session.query(
            extract('month', Bookings.RejectedAt),
            func.count(Bookings.BookingId)
        )
        .filter(Bookings.RejectedAt.isnot(None))
        .group_by(extract('month', Bookings.RejectedAt))
        .all()
    )

    booking_stack_monthly = defaultdict(
        lambda: {'Approved': 0, 'Cancelled': 0, 'Completed': 0, 'Rejected': 0}
    )

    for month, count in approved_rows:
        booking_stack_monthly[int(month)]['Approved'] = count

    for month, count in cancelled_rows:
        booking_stack_monthly[int(month)]['Cancelled'] = count

    for month, count in completed_rows:
        booking_stack_monthly[int(month)]['Completed'] = count

    for month, count in rejected_rows:
        booking_stack_monthly[int(month)]['Rejected'] = count

    booking_months_sorted = sorted(booking_stack_monthly.keys())
    
    booking_status_stack = {
        'labels': [MONTH_LABELS[m - 1] for m in booking_months_sorted],
        'approved': [booking_stack_monthly[m]['Approved'] for m in booking_months_sorted],
        'cancelled': [booking_stack_monthly[m]['Cancelled'] for m in booking_months_sorted],
        'completed': [booking_stack_monthly[m]['Completed'] for m in booking_months_sorted],
        'rejected': [booking_stack_monthly[m]['Rejected'] for m in booking_months_sorted],
    }

    dept_attendance_rows = (
        db.session.query(
            Departments.DepartmentName,
            Attendance.AttendanceStatus,
            func.count(Attendance.AttendanceId)
        )
        .join(Users, Users.DepartmentId == Departments.DepartmentId)
        .join(Bookings, Bookings.UserId == Users.UserId)
        .join(Attendance, Attendance.BookingId == Bookings.BookingId)
        .filter(Attendance.AttendanceStatus.in_(['Attended', 'Absent']))
        .group_by(Departments.DepartmentName, Attendance.AttendanceStatus)
        .all()
    )

    dept_map = defaultdict(lambda: {"Attended": 0, "Absent": 0})

    for dept, status, count in dept_attendance_rows:
        dept_map[dept][status] = count

    dept_rate_rows = []

    for dept, vals in dept_map.items():
        attended = vals["Attended"]
        absent = vals["Absent"]
        total = attended + absent

        rate = round((attended / total) * 100, 1) if total else 0

        dept_rate_rows.append({
            "dept": dept,
            "rate": rate
        })

    dept_rate_rows.sort(key=lambda x: x["rate"], reverse=True)

    dept_attendance_rate = {
        "labels": [d["dept"] for d in dept_rate_rows],
        "data": [d["rate"] for d in dept_rate_rows],
    }

    top_trainers = (
        db.session.query(
            Users,
            func.count(TrainingSessions.SessionId).label("session_count")
        )
        .join(Users.training_sessions)
        .filter(TrainingSessions.Status == 'Completed')
        .group_by(Users.UserId)
        .order_by(func.count(TrainingSessions.SessionId).desc())
        .limit(3)
        .all()
    )

    top_sessions = (
        db.session.query(
            TrainingSessions,
            func.count(Bookings.BookingId).label("booking_count")
        )
        .join(TrainingSessions.bookings)
        .group_by(TrainingSessions.SessionId)
        .order_by(func.count(Bookings.BookingId).desc())
        .limit(3)
        .all()
    )

    top_courses = (
        db.session.query(
            TrainingCourses,
            func.count(Bookings.BookingId).label("booking_count"),
            func.count(distinct(TrainingSessions.SessionId)).label("session_count")
        )
        .join(TrainingCourses.sessions)
        .outerjoin(TrainingSessions.bookings)
        .group_by(TrainingCourses.CourseId)
        .order_by(func.count(Bookings.BookingId).desc())
        .limit(3)
        .all()
    )

    top_learners = (
        db.session.query(
            Users,
            func.count(Attendance.AttendanceId).label("attended_count")
        )
        .join(Users.attendance_records)
        .filter(
            # Users.Role == 'Learner',
            Attendance.AttendanceStatus == 'Attended'
        )
        .group_by(Users.UserId)
        .order_by(func.count(Attendance.AttendanceId).desc())
        .limit(3)
        .all()
    )

    # ── ASSEMBLE chart_data FOR THE TEMPLATE / JS ──────────────────────────
    chart_data = {
        'sessions_by_month': sessions_by_month,
        'sessions_by_dept': sessions_by_dept,
        'attendance_trend': attendance_trend,
        'delivery_split': delivery_split,
        'attendance_stack': attendance_stack,
        'attendance_pie': attendance_pie,
        'booking_funnel': booking_funnel,
        'booking_status_stack': booking_status_stack,
        'dept_attendance_rate': dept_attendance_rate
        # 'rankings': {
        #     'top_trainers': top_trainers,
        #     'bottom_trainers': bottom_trainers,
        #     'top_sessions': top_sessions,
        #     'bottom_sessions': bottom_sessions,
        #     'top_courses': top_courses,
        #     'bottom_courses': bottom_courses,
        #     'top_learners': top_learners,
        #     'bottom_learners': bottom_learners,
        # },
    } 

    print(chart_data['sessions_by_dept'])

    return render_template(
        'reports_and_analytics.html',
        total_sessions=total_sessions,
        total_bookings=total_bookings,
        overall_attendance_rate=overall_attendance_rate,
        overall_no_show_rate=overall_no_show_rate,
        participants=participants,
        completion_rate=completion_rate,
        top_trainers=top_trainers,
        top_sessions=top_sessions,
        top_courses=top_courses,
        top_learners=top_learners,
        chart_data=chart_data,
        upcoming_bookings=upcoming_bookings
    )