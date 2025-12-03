from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from app.models import User
from app.extensions import db, csrf




def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'waniya-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)

    login = LoginManager()
    login.init_app(app)
    login.login_view = "login"

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.booking import booking_bp
    from app.routes.customer import customer_bp
    from app.routes.room import rooms_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(rooms_bp)



    return app
