from flask import Blueprint, render_template,redirect,url_for,flash,session
from app.forms.forms import AdminLoginForm,EmployeeRegistrationForm
# from app.forms.register import RegisterForm
from app.models import User,Employees,Booking,Branch,Room,Admin
from app.extensions import db



from flask import Blueprint, render_template
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('home.html')


@auth_bp.route('/Adminlogin',methods = ['GET','POST'])
def Adminlogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = Admin.query.filter_by(username=username).first()
        
        if user and user.check_password(password):

            session['user_id'] = user.id   
            flash('Login Succesfully','success')
            return redirect(url_for('home.html'))
        else:
            flash('Invalid username or password','danger')
            
    return render_template('login.html',form = form)

@auth_bp.route('/logout')
def logout():
    session.pop('user_id',None)
    flash('logged out','info')
    return redirect(url_for('auth.Adminlogin'))



# # @auth_bp.route('/register',methods = ['GET','POST'])
# # def register():
# #     form = RegisterForm()
# #     if form.validate_on_submit():
# #         username = form.username.data
# #         password = form.password.data
# #         new_User = User(username = username,password = password)
# #         db.session.add(new_User)
# #         db.session.commit()
        
# #         flash('Registered Succesfully','success')
            
# #         return redirect(url_for('auth.login'))
        
            
# #     return render_template('register.html',form = form)
       
@auth_bp.route('/Employee/register', methods=['GET', 'POST'])
def admin_register():
    form = EmployeeRegistrationForm()

    # Populate branch dropdown
    form.branchID.choices = [(b.branchID, b.branch_name) for b in Branch.query.all()]

    if form.validate_on_submit():

        # -----------------------------
        # 1. CREATE EMPLOYEE RECORD
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
            flash(f"Error saving employee: {e}", "danger")
            return render_template("admin_register.html", form=form)

        # -----------------------------
        # 2. CREATE ADMIN LOGIN ACCOUNT
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
            flash(f"Error creating admin login: {e}", "danger")
            return render_template("admin_register.html", form=form)

        # -----------------------------
        # SUCCESS
        # -----------------------------
        flash("Admin registered successfully!", "success")
        return redirect(url_for('auth.Adminlogin'))

    # Print form validation errors to terminal
    if form.errors:
        print("Form validation errors:", form.errors)

    return render_template("admin_register.html", form=form)
