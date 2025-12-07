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

    # Specify foreign_keys to avoid ambiguity
    employees = db.relationship("Employees", backref="branch", lazy=True, foreign_keys="Employees.branchID")
    rooms = db.relationship("Room", backref="branch", lazy=True)
    customers = db.relationship("Customer", backref="branch", lazy=True)

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

    

    # Admin login relationship
    admin_login = db.relationship("Admin", backref="employee", uselist=False)

    def __repr__(self):
        return f"<Employee {self.name}>"

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
# ADMIN LOGIN TABLE
# ==========================================================


class Customer(db.Model):
    __tablename__ = "customer"
    customerID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    cnic = db.Column(db.String(50))
    contact_no = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    gender = db.Column(db.String(10))
    branchID = db.Column(db.Integer, db.ForeignKey("branch.branchID"))

    login = db.relationship(
        "CustomerLogin",
        backref="customer",
        uselist=False,
        foreign_keys="[CustomerLogin.customerID]"
    )
    room_details = db.relationship("RoomDetail", backref="customer", lazy=True)
    bookings = db.relationship("Booking", backref="customer", lazy=True)
    payments = db.relationship("Payment", backref="customer", lazy=True)


class CustomerLogin(db.Model):
    __tablename__ = "customer_login"

    email = db.Column(db.String(120), db.ForeignKey("customer.email"), primary_key=True)
    customerID = db.Column(db.Integer, db.ForeignKey("customer.customerID"))
    customer_name = db.Column(db.String(120))
    pwd = db.Column(db.String(120))


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
    customerID = db.Column(db.Integer, db.ForeignKey("customer.customerID"))

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
    customerID = db.Column(db.Integer, db.ForeignKey("customer.customerID"))
    checkIn = db.Column(db.Date)
    checkOut = db.Column(db.Date)
    no_of_guests = db.Column(db.Integer)
    booking_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20))

    payments = db.relationship("Payment", backref="booking", lazy=True)

    def __repr__(self):
        return f"<Booking {self.bookID}>"


# ==========================================================
# PAYMENT TABLE
# ==========================================================
class Payment(db.Model):
    __tablename__ = "payment"

    paymentID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer, db.ForeignKey("customer.customerID"))
    bookingID = db.Column(db.Integer, db.ForeignKey("booking.bookID"))
    servicesDetailID = db.Column(db.Integer, db.ForeignKey("services_detail.servicesDetailID"))
    total_amount = db.Column(db.Float)
    payment_date = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f"<Payment {self.paymentID}>"
