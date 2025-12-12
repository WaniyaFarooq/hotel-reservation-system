
from app import create_app
from app.extensions import db
from app.models import Employees, Branch, User, Room, Admin, Payment, CustomerLogin
from datetime import date
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # ====================
    # 1. TABLES BANAO PEHLE
    # ====================
    db.create_all()
    print("✅ Tables created")
    
    # ====================
    # 2. BRANCH ADD KARO
    # ====================
    branch = Branch.query.filter_by(branch_name="Main Branch").first()
    if not branch:
        branch = Branch(branch_name="Main Branch", city="Karachi")
        db.session.add(branch)
        db.session.commit()
        print("✅ Branch added")
    else:
        print("⚠️ Branch already exists")
    
    # ====================
    # 3. EMPLOYEE ADD KARO
    # ====================
    employee = Employees.query.filter_by(email="john@example.com").first()
    if not employee:
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
        print("✅ Employee added")
    else:
        print("⚠️ Employee already exists")
    
    # ====================
    # 4. ADMIN LOGIN ADD KARO
    # ====================
    admin = Admin.query.filter_by(username="johndoe").first()
    if not admin:
        admin = Admin(
            empID=employee.empID,
            username="johndoe"
        )
        admin.set_password("password123")
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin login added")
    else:
        print("⚠️ Admin already exists")
    
    # ====================
    # 5. USER ADD KARO
 
    rooms_data = [
        # --------- FLOOR 1: Standard Rooms (101-106) ---------
        (101, "Available", "Standard", 3000),
        (102, "Occupied",  "Standard", 3000),
        (103, "Available", "Standard", 3000),
        (104, "Available", "Standard", 3000),
        (105, "Occupied",  "Standard", 3000),
        (106, "Available", "Standard", 3000),
        
        # --------- FLOOR 2: Deluxe Rooms (201-206) ---------
        (201, "Available", "Deluxe", 5000),
        (202, "Occupied",  "Deluxe", 5000),
        (203, "Available", "Deluxe", 5000),
        (204, "Available", "Deluxe", 5000),
        (205, "Occupied",  "Deluxe", 5000),
        (206, "Available", "Deluxe", 5000),
        
        # --------- FLOOR 3: Executive Rooms (301-306) ---------
        (301, "Available", "Executive", 7000),
        (302, "Occupied",  "Executive", 7000),
        (303, "Available", "Executive", 7000),
        (304, "Available", "Executive", 7000),
        (305, "Occupied",  "Executive", 7000),
        (306, "Available", "Executive", 7000),
        
        # --------- FLOOR 4: Suite Rooms (401-406) ---------
        (401, "Available", "Suite", 10000),
        (402, "Occupied",  "Suite", 10000),
        (403, "Available", "Suite", 10000),
        (404, "Available", "Suite", 10000),
        (405, "Occupied",  "Suite", 10000),
        (406, "Available", "Suite", 10000),
        
        # --------- FLOOR 5: VIP/Presidential Rooms (501-506) ---------
        (501, "Available", "Presidential", 15000),
        (502, "Occupied",  "Presidential", 15000),
        (503, "Available", "Presidential", 15000),
        (504, "Available", "Presidential", 15000),
        (505, "Occupied",  "Presidential", 15000),
        (506, "Available", "Presidential", 15000),
    ]
    
    added_count = 0
    for r in rooms_data:
        existing_room = Room.query.filter_by(roomID=r[0]).first()
        if not existing_room:
            room = Room(
                roomID=r[0],
                status=r[1],
                room_type=r[2],
                price=r[3],
                branchID=branch.branchID
            )
            db.session.add(room)
            added_count += 1
    
    if added_count > 0:
        db.session.commit()
        print(f"✅ {added_count} rooms added")
        
        # Summary print karo
        print("\n📊 ROOM SUMMARY:")
        print("=" * 40)
        print("Floor 1 (101-106): 6 Standard Rooms")
        print("Floor 2 (201-206): 6 Deluxe Rooms")  
        print("Floor 3 (301-306): 6 Executive Rooms")
        print("Floor 4 (401-406): 6 Suite Rooms")
        print("Floor 5 (501-506): 6 Presidential Rooms")
        print("=" * 40)
        print(f"Total: 30 rooms across 5 floors")
        
        # Type-wise breakdown
        print("\n🏨 ROOM TYPE DISTRIBUTION:")
        room_types = {}
        for r in rooms_data:
            room_type = r[2]
            room_types[room_type] = room_types.get(room_type, 0) + 1
        
        for room_type, count in room_types.items():
            print(f"  {room_type}: {count} rooms")
            
        # Status-wise breakdown  
        print("\n📈 AVAILABILITY STATUS:")
        available = sum(1 for r in rooms_data if r[1] == "Available")
        occupied = sum(1 for r in rooms_data if r[1] == "Occupied")
        print(f"  Available: {available} rooms")
        print(f"  Occupied: {occupied} rooms")
        
    else:
        print("⚠️ All rooms already exist")
    
    print("\n🎉 Database seeding complete!")

    # Add to seed.py

    for i in range(1, 6):
        p = Payment(
            customerID=1, 
            bookingID=1, 
            total_amount=(i * 1000), 
            payment_date=date.today()
        )
        db.session.add(p)

    db.session.commit()
    print("Payments added for revenue page!")

    # ====================
    # CUSTOMERS ADD KARO
    # ====================
    print("\n👤 Adding customers...")
    customers = [
     
        CustomerLogin(
            email="fatima.ali@yahoo.com",
            customer_name="Fatima Ali",
            password_hash=generate_password_hash("password456")
        ),
        CustomerLogin(
            email="bilal.ahmed@outlook.com",
            customer_name="Bilal Ahmed",
            password_hash=generate_password_hash("password789")
        ),
        CustomerLogin(
            email="zainab.khan@gmail.com",
            customer_name="Zainab Khan",
            password_hash=generate_password_hash("password101")
        ),
        CustomerLogin(
            email="usman.hassan@hotmail.com",
            customer_name="Usman Hassan",
            password_hash=generate_password_hash("password202")
        )
    ]

    for customer in customers:
        existing = CustomerLogin.query.filter_by(email=customer.email).first()
        if not existing:
            db.session.add(customer)
            print(f"  ✓ Added: {customer.customer_name}")
        else:
            print(f"  ⚠️ Already exists: {customer.customer_name}")

    db.session.commit()
    print("✅ Customers added successfully!")