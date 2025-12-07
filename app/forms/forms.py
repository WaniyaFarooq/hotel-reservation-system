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