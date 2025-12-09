from flask import Flask
from flask_login import LoginManager
from app.extensions import db, csrf

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    # Configuration
    app.config['SECRET_KEY'] = 'waniya-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    csrf.init_app(app)

    # Setup login manager
    setup_login_manager(app)

    # register_blueprints(app)#from conflict
    
    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    # from .routes.booking import booking_bp
    from .routes.customer import customer_bp
    from .routes.rooms import rooms_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    # app.register_blueprint(booking_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(rooms_bp)
    return app

def setup_login_manager(app):
    """Configure Flask-Login"""
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # Use blueprint prefix
    
    @login_manager.user_loader
    def load_user(user_id):
        # Import inside function to avoid circular imports
        from app.models import User
        return User.query.get(int(user_id))
    


