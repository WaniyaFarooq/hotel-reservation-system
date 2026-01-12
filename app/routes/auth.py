from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.forms.forms import AdminLoginForm, EmployeeRegistrationForm
from app.models import Employees, Branch, Admin
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

# ---------------------------------------
# HOME PAGE
# ---------------------------------------
@auth_bp.route('/')
def home():
    return render_template('home.html')


# ---------------------------------------
# ADMIN LOGIN
# ---------------------------------------
@auth_bp.route('/Adminlogin', methods=['GET', 'POST'])
def Adminlogin():
    form = AdminLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            session['user_id'] = admin.userID
            flash('Login successfully', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('Admin_login.html', form=form)


# ---------------------------------------
# LOGOUT
# ---------------------------------------
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out', 'info')
    return redirect(url_for('auth.Adminlogin'))


# ---------------------------------------
# ADMIN REGISTRATION
# ---------------------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def admin_register():

    # # Simple login protection (NO route name changes)
    # if 'user_id' not in session:
    #     flash('Please login first', 'warning')
    #     return redirect(url_for('auth.Adminlogin'))

    form = EmployeeRegistrationForm()

    # Populate branch dropdown
    form.branchID.choices = [
        (b.branchID, b.branch_name) for b in Branch.query.all()
    ]

    if form.validate_on_submit():

        # -----------------------------
        # 1. CREATE EMPLOYEE
        # -----------------------------
        new_employee = Employees(
            name=form.name.data,
            phone_no=form.phone_no.data,
            email=form.email.data,
            designation=form.designation.data,
            joining_date=form.joining_date.data,
            address=form.address.data,
            branchID=form.branchID.data
        )

        try:
            db.session.add(new_employee)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error saving employee: {e}", "error")
            return render_template("admin_register.html", form=form)

        # -----------------------------
        # 2. CREATE ADMIN ACCOUNT
        # -----------------------------
        new_admin = Admin(
            empID=new_employee.empID,
            username=form.username.data
        )
        new_admin.set_password(form.password.data)

        try:
            db.session.add(new_admin)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating admin login: {e}", "error")
            return render_template("admin_register.html", form=form)

        flash("Admin registered successfully!", "success")
        return redirect(url_for('auth.Adminlogin'))

    if form.errors:
        flash(f"{form.errors}", "error")
        print("Form validation errors:", form.errors)

    return render_template("admin_register.html", form=form)


# ---------------------------------------
# STATIC PAGES
# ---------------------------------------
@auth_bp.route('/contact')
def contact():
    return render_template('contact.html')


@auth_bp.route('/about')
def about():
    return render_template('about.html')


@auth_bp.route('/Rooms')
def Rooms():
    return render_template('rooms.html')
