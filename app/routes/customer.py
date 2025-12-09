from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.forms.forms import CustomerLoginForm, CustomerRegistrationForm
from app.models import CustomerLogin
from app.extensions import db

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = CustomerLoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = CustomerLogin.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.customerID
            flash('Login successfully!', 'success')
            return redirect(url_for('auth.home'))  # FIXED
        else:
            flash('Invalid email or password', 'danger')

    return render_template('customer_login.html', form=form)


@customer_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out', 'info')
    return redirect(url_for('customer.login'))


@customer_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = CustomerRegistrationForm()

    if form.validate_on_submit():

        # Check if email exists
        existing = CustomerLogin.query.filter_by(email=form.email.data).first()
        if existing:
            flash("Email already registered!", "warning")
            return render_template("customer_register.html", form=form)

        new_customer = CustomerLogin(
            email=form.email.data,
            customer_name=form.name.data
        )

        new_customer.set_password(form.password.data)

        try:
            db.session.add(new_customer)
            db.session.commit()
            flash("Customer registered successfully!", "success")
            return redirect(url_for('customer.login'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error saving customer: {e}", "danger")

    return render_template("customer_register.html", form=form)
