

from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Service, TimeSlot, Booking, User, ServiceProvider
from flask_jwt_extended import jwt_required, get_jwt 
from models import db, DayOfWeek



routes = Blueprint('routes', __name__)

@routes.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([service.name for service in services]), 200

@routes.route('/services/<int:id>/timeslots', methods=['GET'])
def get_timeslots(id):
    timeslots = TimeSlot.query.filter_by(service_id=id).all()
    return jsonify([{
        "day_of_week": ts.day_of_week,
        "start_time": ts.start_time,
        "end_time": ts.end_time,
        "vacancies": ts.vacancies
    } for ts in timeslots]), 200

@routes.route('/bookings', methods=['POST'])
@jwt_required()
def book_timeslot():
    user_id = get_jwt_identity()
    data = request.get_json()
    timeslot = TimeSlot.query.get(data['timeslot_id'])
    if timeslot.vacancies > 0:
        booking = Booking(user_id=user_id, timeslot_id=timeslot.id)
        timeslot.book_timeslot()  # Reduce vacancies
        db.session.add(booking)
        db.session.commit()
        return jsonify({"message": "Booking confirmed"}), 201
    return jsonify({"message": "No vacancies available"}), 400

@routes.route('/users/<int:id>/bookings', methods=['GET'])
@jwt_required()
def get_user_bookings(id):
    if id != get_jwt_identity():
        return jsonify({"message": "Forbidden"}), 403
    bookings = Booking.query.filter_by(user_id=id).all()
    return jsonify([{
        "timeslot_id": booking.timeslot_id,
        "status": booking.status
    } for booking in bookings]), 200

 # Make sure this is imported
@routes.route('/routes/services', methods=['POST'])
@jwt_required()
def create_service():
    service_provider_id = get_jwt_identity()  # Extract service provider ID from JWT

    data = request.get_json()

    if not service_provider_id:
        return jsonify({"message": "Service provider not found in the token"}), 400

    new_service = Service(
        service_provider_id=service_provider_id,
        name=data['name'],
        description=data.get('description', '')
    )

    try:
        db.session.add(new_service)
        db.session.commit()
        return jsonify({"message": "Service created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500



@routes.route('/services/<int:id>', methods=['GET'])
def get_service_by_id(id):
    service = Service.query.get(id)
    if not service:
        return jsonify({"message": "Service not found"}), 404

    return jsonify({
        "id": service.id,
        "name": service.name,
        "description": service.description
    }), 200


@routes.route('/services/<int:id>/timeslots', methods=['POST'])
@jwt_required()
def create_timeslot(id):
    data = request.get_json()
    try:
        # Make sure to map the day_of_week to the correct enum value
        day_of_week_enum = DayOfWeek[data['day_of_week']]  # This maps string to enum
        new_timeslot = TimeSlot(
            service_id=id,
            day_of_week=day_of_week_enum,
            start_time=data['start_time'],
            end_time=data['end_time'],
            vacancies=data['vacancies']
        )
        db.session.add(new_timeslot)
        db.session.commit()
        return jsonify({"message": "Timeslot created successfully"}), 201
    except KeyError:
        return jsonify({"message": "Invalid day_of_week value"}), 400
    

@routes.route('/bookings/<int:id>', methods=['PUT'])
@jwt_required()
def update_booking_status(id):
    user = get_jwt_identity()
    if user['role'] != 'provider':
        return jsonify({"message": "Access denied"}), 403

    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    data = request.get_json()
    new_status = data.get('status')
    if new_status not in ['approved', 'completed', 'canceled']:
        return jsonify({"message": "Invalid status"}), 400

    booking.status = new_status
    db.session.commit()

    return jsonify({"message": "Booking status updated successfully"}), 200

