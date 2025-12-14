from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField ,SelectField,DateField
from wtforms.validators import DataRequired, Length ,Optional,Email

class AdminLoginForm(FlaskForm):
    
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=3, max=25)
    ])
    password = PasswordField("Password", validators=[
        DataRequired()
    ])
    submit = SubmitField("Login")

class EmployeeRegistrationForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    phone_no = StringField("Phone Number", validators=[Optional(), Length(max=50)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    designation = StringField("Designation", validators=[Optional(), Length(max=120)])

    joining_date = DateField("Joining Date", format="%Y-%m-%d", validators=[Optional()])
    address = StringField("Address", validators=[Optional(), Length(max=255)])
    branchID = SelectField("Branch", coerce=int, validators=[Optional()])  # Populated dynamically
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")
    
class CustomerLoginForm(FlaskForm):
    
    email = StringField("email", validators=[
        DataRequired(), Email(), Length(max=120)
    ])
    password = PasswordField("Password", validators=[
        DataRequired()
    ])
    submit = SubmitField("Login")
    
class CustomerRegistrationForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")
    
from wtforms import IntegerField

class BookingForm(FlaskForm):
    room_id = SelectField("Room", coerce=int, validators=[DataRequired()])
    checkIn = DateField("Check-In Date", format="%Y-%m-%d", validators=[DataRequired()])
    checkOut = DateField("Check-Out Date", format="%Y-%m-%d", validators=[DataRequired()])
    guests = IntegerField("Number of Guests", validators=[DataRequired()])
    submit = SubmitField("Book Now")

class PaymentForm(FlaskForm):
    submit = SubmitField("Pay Now")
    
class RevenueFilterForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', render_kw={"type": "date"})
    end_date = DateField('End Date', format='%Y-%m-%d', render_kw={"type": "date"})
    submit = SubmitField('Filter')