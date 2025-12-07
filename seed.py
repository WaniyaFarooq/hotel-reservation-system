from app import create_app
from app.extensions import db
from app.models import Employees, Branch, User
from datetime import date

app = create_app()
app.app_context().push()  # push app context for db operations

# Add branch
branch = Branch(branch_name="Main Branch", city="Karachi")
db.session.add(branch)
db.session.commit()

# Add employee
employee = Employees(
    name="John Doe",
    phone_no="03001234567",
    email="john@example.com",
    designation="Manager",
    joining_date=date.today(),
    address="123 Street",
    branchID=branch.branchID
)
db.session.add(employee)
db.session.commit()

# Add user login
user = User(username="johndoe")
user.set_password("password123")
db.session.add(user)
db.session.commit()

print("Data added successfully!")
