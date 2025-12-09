from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models import Room

rooms_bp = Blueprint("rooms", __name__)

@rooms_bp.route("/rooms")
def rooms():
    all_rooms = Room.query.all()
    
    # Calculate counts
    available = 0
    occupied = 0
    for room in all_rooms:
        status_lower = str(room.status).lower()

        if room.status == 'available':
            available += 1
        elif room.status == 'occupied':
            occupied += 1
        
    other = len(all_rooms) - available - occupied
    
    return render_template("room_details.html", 
                         rooms=all_rooms,
                         available=available,
                         occupied=occupied,
                         other=other)



@rooms_bp.route("/add-room", methods=["GET", "POST"])
def add_room():
    if request.method == "POST":
        room = Room(
            status=request.form.get("status", "available"),
            type=request.form["type"],
            price=float(request.form["price"]),
            branchID=int(request.form.get("branchID", 1))
        )
        db.session.add(room)
        db.session.commit()
        # return redirect(url_for("rooms.rooms"))
        return redirect("/admin/rooms")  
    
    # You need to CREATE this template:
    return render_template("add_rooms.html")  # This template doesn't exist!
