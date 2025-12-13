from app.extensions import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# ==========================================================
# USER TABLE
# ==========================================================
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)


# ==========================================================
# BRANCH TABLE
# ==========================================================
class Branch(db.Model):
    __tablename__ = 'branch'

    branchID = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    managerID = db.Column(db.Integer, db.ForeignKey("employees.empID"))

    employees = db.relationship("Employees", backref="branch", lazy=True, foreign_keys="Employees.branchID")
    rooms = db.relationship("Room", backref="branch", lazy=True)

    def __repr__(self):
        return f"<Branch {self.branch_name} - {self.city}>"


# ==========================================================
# EMPLOYEES TABLE
# ==========================================================
class Employees(db.Model):
    __tablename__ = 'employees'

    empID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone_no = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    designation = db.Column(db.String(120))
    joining_date = db.Column(db.Date)
    address = db.Column(db.String(255))
    branchID = db.Column(db.Integer, db.ForeignKey("branch.branchID"))

    admin_login = db.relationship("Admin", backref="employee", uselist=False)

    def __repr__(self):
        return f"<Employee {self.name}>"


# ==========================================================
# ADMIN LOGIN TABLE
# ==========================================================
class Admin(db.Model):
    __tablename__ = "admin_login"

    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empID = db.Column(db.Integer, db.ForeignKey("employees.empID"), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)


# ==========================================================
# CUSTOMER LOGIN ONLY (no Customer table)
# ==========================================================
class CustomerLogin(db.Model):
    __tablename__ = "customer_login"

    customerID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    customer_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ==========================================================
# SERVICES TABLE
# ==========================================================
class Services(db.Model):
    __tablename__ = "services"

    servicesID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)

    service_details = db.relationship("ServicesDetail", backref="service", lazy=True)

    def __repr__(self):
        return f"<Service {self.name}>"


# ==========================================================
# ROOM TABLE
# ==========================================================
class Room(db.Model):
    __tablename__ = "room"

    roomID = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))
    type = db.Column(db.String(120))
    price = db.Column(db.Float)
    branchID = db.Column(db.Integer, db.ForeignKey("branch.branchID"))

    room_details = db.relationship("RoomDetail", backref="room", lazy=True)

    @property
    def id(self):
        return self.roomID
    
    @property
    def number(self):
        return self.roomID
    
    @property
    def available(self):
        return self.status == "available"

    def __repr__(self):
        return f"<Room {self.roomID}>"


# ==========================================================
# ROOM DETAIL TABLE
# ==========================================================
class RoomDetail(db.Model):
    __tablename__ = "room_detail"

    roomDetailID = db.Column(db.Integer, primary_key=True)
    roomID = db.Column(db.Integer, db.ForeignKey("room.roomID"))
    bookingID = db.Column(db.Integer, db.ForeignKey("booking.bookID"))
    customerID = db.Column(db.Integer, db.ForeignKey("customer_login.customerID"))

    services_detail = db.relationship("ServicesDetail", backref="room_detail", lazy=True)

    def __repr__(self):
        return f"<RoomDetail {self.roomDetailID}>"


# ==========================================================
# SERVICES DETAIL TABLE
# ==========================================================
class ServicesDetail(db.Model):
    __tablename__ = "services_detail"

    servicesDetailID = db.Column(db.Integer, primary_key=True)
    roomDetailID = db.Column(db.Integer, db.ForeignKey("room_detail.roomDetailID"))
    serviceID = db.Column(db.Integer, db.ForeignKey("services.servicesID"))
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)

    payments = db.relationship("Payment", backref="services_detail", lazy=True)

    def __repr__(self):
        return f"<ServicesDetail {self.servicesDetailID}>"


# ==========================================================
# BOOKING TABLE
# ==========================================================
class Booking(db.Model):
    __tablename__ = "booking"

    bookID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer, db.ForeignKey("customer_login.customerID"))
    checkIn = db.Column(db.Date)
    checkOut = db.Column(db.Date)
    no_of_guests = db.Column(db.Integer)
    booking_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20))

    payments = db.relationship("Payment", backref="booking", lazy=True)

    def __repr__(self):
        return f"<Booking {self.bookID}>"


# =====================================================
# PAYMENT TABLE
# =====================================================
class Payment(db.Model):
    __tablename__ = "payment"

    paymentID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer, db.ForeignKey("customer_login.customerID"), nullable=False)
    bookingID = db.Column(db.Integer, db.ForeignKey("booking.bookID"), nullable=False)
    servicesDetailID = db.Column(db.Integer, db.ForeignKey("services_detail.servicesDetailID"), nullable=True)  # <-- add this
    payment_date = db.Column(db.Date, default=datetime.utcnow)
    room_amount = db.Column(db.Float, nullable=False, default=0.0)
    services_amount = db.Column(db.Float, nullable=False, default=0.0)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(20), default="Pending")
