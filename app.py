import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate() 

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', 'lmrsecret')

    db.init_app(app)
    migrate.init_app(app, db)

    from routes import register_routes
    register_routes(app)

    return app