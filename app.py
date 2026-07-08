import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

load_dotenv(override=True)

db = SQLAlchemy()
migrate = Migrate() 

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', 'lmrsecret')
    app.config["RESEND_API_KEY"] = os.getenv('RESEND_API_KEY')

    db.init_app(app) 
    migrate.init_app(app, db)

    from routes import register_routes
    register_routes(app, db)

    @app.template_filter("format_datetime")
    def format_datetime(dt):
        if dt is None:
            return ""
        return dt.astimezone().strftime("%d %b %Y, %I:%M %p")
    
    # context processor inject variables into every template automatically so 'unread_notifications_count' is available in base.html on every page.
    @app.context_processor
    def inject_unread_notifications():
        from flask import session
        from models import Notifications

        if 'user_id' not in session:
            return {"unread_notifications_count": 0}

        count = Notifications.query.filter_by(
            UserId=session['user_id'],
            IsRead=False
            ).count() 

        return {"unread_notifications_count": count}       

    return app