from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.extensions import db
from app.models import Employees, Room, Customer, Booking, Payment, Admin
from datetime import datetime, date
from werkzeug.security import generate_password_hash
from app.forms.forms import EmployeeRegistrationForm 

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ============================
# ADMIN DASHBOARD
# ============================
@admin_bp.route("/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

# ============================
# VIEW STAFF - SIMPLE VERSION
# ============================
@admin_bp.route("/staff")
def view_staff():
    staff = Employees.query.all()
    return render_template("view_staff.html",staff=staff)  # ✅ Just render template

# ============================
# ADD STAFF (WITH AUTO ADMIN LOGIN CREATION)
# ============================
@admin_bp.route("/staff/add", methods=["GET", "POST"])
def add_staff():
    if request.method == "POST":
        try:
            # =====================================
            # 1. FIRST CREATE EMPLOYEE RECORD
            # =====================================
            new_staff = Employees(
                name=request.form["name"],
                phone_no=request.form.get("phone", ""),
                email=request.form["email"],
                designation=request.form["designation"],
                joining_date=datetime.strptime(request.form["joining_date"], "%Y-%m-%d"),
                address=request.form.get("address", ""),
                branchID=int(request.form.get("branchID", 1))  # Default to branch 1
            )
            
            db.session.add(new_staff)
            db.session.flush()  # Get the empID without committing
            
            # =====================================
            # 2. CREATE ADMIN LOGIN AUTOMATICALLY
            # =====================================
            username = request.form["username"]
            password = request.form["password"]
            
            # Check if username already exists
            existing_admin = Admin.query.filter_by(username=username).first()
            if existing_admin:
                flash(f'Username "{username}" already exists. Choose another.', 'danger')
                return redirect(url_for("admin.add_staff"))
            
            # Create admin login
            new_admin = Admin(
                empID=new_staff.empID,  # Use the empID from newly created employee
                username=username
            )
            new_admin.set_password(password)
            
            db.session.add(new_admin)
            db.session.commit()
            
            flash(f'Staff member added successfully! Login: {username}', 'success')
            return redirect(url_for("admin.view_staff"))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding staff: {str(e)}', 'danger')
            return redirect(url_for("admin.add_staff"))
    
    # GET request - show form
    return render_template("add_staff.html")


# ============================
# ROOM DETAILS
# ============================
@admin_bp.route("/rooms")
def room_details():
    rooms = Room.query.all()
    # return render_template("room_details.html", rooms=rooms)
    # Add these counts
    available = 0
    occupied = 0
    for room in rooms:
        if room.status == 'available':
            available += 1
        elif room.status == 'occupied':
            occupied += 1
    
    return render_template("room_details.html", 
                         rooms=rooms,
                         available=available,
                         occupied=occupied)

# ============================
# CUSTOMER DETAILS
# ============================
@admin_bp.route("/customers")
def customer_details():
    customers = Customer.query.all()
    return render_template("customer_details.html", customers=customers)

# ============================
# REVENUE
# ============================
@admin_bp.route("/revenue")
def revenue():
    payments = Payment.query.all()
    
    # Calculate totals
    total_revenue = sum([p.total_amount for p in payments if p.total_amount])
    
    # Today's revenue
    today = date.today()
    today_revenue = sum([
        p.total_amount for p in payments 
        if p.total_amount and p.payment_date == today
    ])
    
    # This month's revenue
    current_month = datetime.now().month
    current_year = datetime.now().year
    month_revenue = sum([
        p.total_amount for p in payments 
        if p.total_amount and p.payment_date and 
        p.payment_date.month == current_month and 
        p.payment_date.year == current_year
    ])
    
    return render_template(
        "revenue.html",
        payments=payments,
        total_revenue=total_revenue or 0,
        today_revenue=today_revenue or 0,
        month_revenue=month_revenue or 0
    )