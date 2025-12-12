from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.forms.forms import CustomerLoginForm, CustomerRegistrationForm, BookingForm
from app.models import CustomerLogin, Booking, Room, Payment, RoomDetail
from app.extensions import db

customer_bp = Blueprint('customer', __name__, url_prefix="/customer")


# ---------------------------------------
# Login
# ---------------------------------------
@customer_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = CustomerLoginForm()

    if form.validate_on_submit():
        user = CustomerLogin.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            session['customer_id'] = user.customerID
            flash('Login successfully!', 'success')
            return redirect(url_for('customer.dashboard'))

        flash('Invalid email or password', 'danger')

    return render_template('customer_login.html', form=form)


# ---------------------------------------
# Logout
# ---------------------------------------
@customer_bp.route('/logout')
def logout():
    session.pop('customer_id', None)
    flash('Logged out', 'info')
    return redirect(url_for('customer.login'))


# ---------------------------------------
# Register
# ---------------------------------------
@customer_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = CustomerRegistrationForm()

    if form.validate_on_submit():

        # Prevent duplicate emails
        if CustomerLogin.query.filter_by(email=form.email.data).first():
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


# ---------------------------------------
# Dashboard
# ---------------------------------------
@customer_bp.route('/dashboard')
def dashboard():
    if 'customer_id' not in session:
        return redirect(url_for('customer.login'))

    customer_id = session['customer_id']

    bookings = Booking.query.filter_by(customerID=customer_id).all()
    payments = Payment.query.filter_by(customerID=customer_id).all()

    return render_template("customer_dashboard.html",
                           bookings=bookings,
                           payments=payments)


# ---------------------------------------
# Book a Room
# ---------------------------------------
@customer_bp.route("/book", methods=["GET", "POST"])
def book():
    if 'customer_id' not in session:
        return redirect(url_for('customer.login'))

    form = BookingForm()
    form.room_id.choices = [(r.roomID, f"{r.type} - Rs.{r.price}") for r in Room.query.all()]

    if form.validate_on_submit():

        # Create booking
        new_booking = Booking(
            customerID=session["customer_id"],
            checkIn=form.checkIn.data,
            checkOut=form.checkOut.data,
            no_of_guests=form.guests.data,
            status="Pending"
        )
        db.session.add(new_booking)
        db.session.commit()

        # Link booking → room
        room_detail = RoomDetail(
            roomID=form.room_id.data,
            bookingID=new_booking.bookID,
            customerID=session["customer_id"]
        )
        db.session.add(room_detail)
        db.session.commit()

        flash("Room booked successfully!", "success")
        return redirect(url_for("customer.dashboard"))

    return render_template("customer_booking.html", form=form)


# ---------------------------------------
# Cancel Booking
# ---------------------------------------
@customer_bp.route("/cancel/<int:booking_id>")
def cancel_booking(booking_id):
    if 'customer_id' not in session:
        return redirect(url_for('customer.login'))

    booking = Booking.query.get_or_404(booking_id)

    # Ensure user can only cancel their own booking
    if booking.customerID != session["customer_id"]:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("customer.dashboard"))

    # Delete linked room details
    RoomDetail.query.filter_by(bookingID=booking.bookID).delete()

    db.session.delete(booking)
    db.session.commit()

    flash("Booking cancelled.", "info")
    return redirect(url_for('customer.dashboard'))


# ---------------------------------------
# Make Payment
# ---------------------------------------
@customer_bp.route("/payment/<int:booking_id>", methods=["GET", "POST"])
def payment(booking_id):
    if 'customer_id' not in session:
        return redirect(url_for('customer.login'))

    booking = Booking.query.get_or_404(booking_id)

    # Calculate room charges
    room_detail = RoomDetail.query.filter_by(bookingID=booking_id).first()
    room_amount = room_detail.room.price if room_detail else 0

    # Calculate services charges
    services_details = room_detail.services_detail if room_detail else []
    services_amount = sum(sd.total_price for sd in services_details)

    total_amount = room_amount + services_amount

    if request.method == "POST":
        new_payment = Payment(
            customerID=session["customer_id"],
            bookingID=booking.bookID,
            room_amount=room_amount,
            services_amount=services_amount,
            total_amount=total_amount,
            status="Paid"
        )
        db.session.add(new_payment)
        db.session.commit()

        flash("Payment successful!", "success")
        return redirect(url_for("customer.dashboard"))

    return render_template("customer_payment.html",
                           booking=booking,
                           room_amount=room_amount,
                           services_amount=services_amount,
                           total_amount=total_amount)
