from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Hospital, Appointment, PatientRecord
from app.schemas import UserSchema, HospitalSchema, AppointmentSchema
from app.utils.decorators import roles_required
from app.extensions import db
from app.utils.responses import respond
from sqlalchemy import or_
from app.services.appointment_service import AppointmentService

api_bp = Blueprint('api', __name__)
user_schema = UserSchema()
hospital_schema = HospitalSchema()
appointment_schema = AppointmentSchema()

# Hospitals Endpoints
@api_bp.route('/hospitals', methods=['GET'])
@jwt_required()
def get_hospitals():
    try:
        hospitals = Hospital.query.all()
        return jsonify([hospital.to_dict() for hospital in hospitals])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/hospitals', methods=['POST'])
@jwt_required()
@roles_required('admin')
def create_hospital():
    data = request.get_json()
    errors = hospital_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    hospital = Hospital(**data)
    db.session.add(hospital)
    db.session.commit()
    return hospital_schema.dump(hospital), 201

# Appointments Endpoints


@api_bp.route('/appointments', methods=['POST', 'GET'])  
@jwt_required()
def appointments():
    if request.method == 'POST':
        data = request.get_json()
        data['patient_id'] = get_jwt_identity()
        errors = appointment_schema.validate(data)
        if errors:
            return respond(errors, 400)
    
        result, status = AppointmentService.create_appointment(data)
        return respond(result, status)
    elif request.method == 'GET':
        current_user = User.query.get(get_jwt_identity())
        
        if current_user.role == 'admin':
            appointments = Appointment.query.all()
        elif current_user.role == 'doctor':
            appointments = Appointment.query.filter_by(doctor_id=current_user.id)
        elif current_user.role == 'patient':
            appointments = Appointment.query.filter_by(patient_id=current_user.id)
        else:
            return jsonify({"error": "Unauthorized"}), 403

        return jsonify([appointment_schema.dump(appt) for appt in appointments])


@api_bp.route('/appointments/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def single_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    current_user = User.query.get(get_jwt_identity())

    if request.method == 'GET':
        if current_user.role == 'patient' and appointment.patient_id != current_user.id:
            return jsonify({"error": "Unauthorized"}), 403
        if current_user.role == 'doctor' and appointment.doctor_id != current_user.id:
            return jsonify({"error": "Unauthorized"}), 403
        return appointment_schema.dump(appointment)
    
    elif request.method == 'PUT':
        appointment = Appointment.query.get_or_404(id)
        current_user = User.query.get(get_jwt_identity())    
        # Authorization check
        if current_user.role == 'doctor' and appointment.doctor_id != current_user.id:
            return jsonify({"error": "Unauthorized"}), 403
        
        data = request.get_json()
        errors = appointment_schema.validate(data, partial=True)
        if errors:
            return jsonify(errors), 400
        
        for key, value in data.items():
            setattr(appointment, key, value)
        
        db.session.commit()
        return appointment_schema.dump(appointment)
        
    # elif request.method == 'DELETE':
        # Add delete logic


# Patient Records Endpoints
@api_bp.route('/patient-records', methods=['GET'])
@jwt_required()
@roles_required('doctor', 'admin')
def get_patient_records():
    records = PatientRecord.query.all()
    return jsonify([{
        'id': r.id,
        'patient': r.patient.username,
        'doctor': r.doctor.username,
        'diagnosis': r.diagnosis,
        'treatment_plan': r.treatment_plan
    } for r in records])

# Users Endpoints
@api_bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
@roles_required('admin')
def get_user(id):
    user = User.query.get_or_404(id)
    return user_schema.dump(user)

@api_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
@roles_required('admin')
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    errors = user_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400
    
    for key, value in data.items():
        if key == 'password':
            user.password = bcrypt.generate_password_hash(value).decode('utf-8')
        else:
            setattr(user, key, value)
    
    db.session.commit()
    return user_schema.dump(user)


@api_bp.route('/appointments/<int:id>', methods=['GET'])
@jwt_required()
def get_appointment(id):
    try:
        appointment = Appointment.query.get_or_404(id)
        current_user = User.query.get(get_jwt_identity())
        
        # Authorization check
        if current_user.role == 'patient' and appointment.patient_id != current_user.id:
            return jsonify({"error": "Unauthorized"}), 403
        if current_user.role == 'doctor' and appointment.doctor_id != current_user.id:
            return jsonify({"error": "Unauthorized"}), 403

        return appointment_schema.dump(appointment), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500