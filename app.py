from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect


csrf = CSRFProtect()

#created database object globally
# You are creating a database object. But right now → it is empty, not connected to any Flask app.
db = SQLAlchemy()


# You are creating a function that will build and return the Flask app object.
def create_app():
    app = Flask(__name__) # flask app k instance
    # A secret key used by Flask to:protect sessions,protect cookies,protect CSRF tokens (forms protection)
    app.config['SECRET_KEY'] = 'waniya-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
    # Use SQLite database named todo.db and store it in project folder.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # to connect db to app
    # db.__init__(app)
    db.init_app(app)
    csrf.init_app(app)
    
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
    # Add all task/auth routes to my main Flask application
    # mini app ki tarah related routes 
   
    return app
    

