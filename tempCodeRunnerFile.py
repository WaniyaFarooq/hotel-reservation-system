from app import create_app
from app.extensions import db, csrf

from app.models import User, Branch,Employees ,AdminLogin,Customer,CustomerLogin,Services,Room,RoomDetail,ServicesDetail,Booking,Payment

app = create_app()

with app.app_context():
    db.create_all()   # <-- TABLES GET CREATED HERE

if __name__ == "__main__":
    app.run(debug=True)