# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import CSRFProtect
# from flask_login import LoginManager
# from app.models import User
# from app.extensions import db, csrf



# def create_app():
#     app = Flask(
#         __name__,
#         template_folder="templates",
#         static_folder="static"
#     )

#     app.config['SECRET_KEY'] = 'waniya-key'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     # Initialize extensions
#     db.init_app(app)
#     csrf.init_app(app)

#     login = LoginManager()
#     login.init_app(app)
#     login.login_view = "login"

#     @login.user_loader
#     def load_user(user_id):
#         return User.query.get(int(user_id))

#     # Register blueprints
#     from .routes.auth import auth_bp
#     # from .routes.admin import admin_bp
#     # from .routes.booking import booking_bp
#     # from .routes.customer import customer_bp
#     # from .routes.rooms import rooms_bp

#     app.register_blueprint(auth_bp)
#     # app.register_blueprint(admin_bp)
#     # app.register_blueprint(booking_bp)
#     # app.register_blueprint(customer_bp)
#     # app.register_blueprint(rooms_bp)

#     from app.routes.rooms import rooms_bp
#     app.register_blueprint(rooms_bp)



#     return app

# app/__init__.py





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
    
    # Register blueprints
    register_blueprints(app)

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

def register_blueprints(app):
    """Register all application blueprints"""
    # Import blueprints here (inside function to avoid circular imports)
    from app.routes.auth import auth_bp
    from app.routes.rooms import rooms_bp
    # Import other blueprints when ready:
    from app.routes.admin import admin_bp
    # from app.routes.booking import booking_bp
    # from app.routes.customer import customer_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(admin_bp)
    # app.register_blueprint(booking_bp)
    # app.register_blueprint(customer_bp)
    
    print("✓ Blueprints registered successfully!")