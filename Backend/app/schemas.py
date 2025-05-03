from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    role = fields.Str(validate=validate.OneOf(['admin', 'doctor', 'patient']))

class HospitalSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)

class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    hospital_id = fields.Int(required=True)
    appointment_date = fields.Date(required=True)
    purpose = fields.Str(required=True)
    status = fields.Str(validate=validate.OneOf(['pending', 'confirmed', 'cancelled', 'completed']))
    
    
    def validate_appointment_date(self, value):
        if value < datetime.now():
            raise ValidationError("Appointment date cannot be in the past")
        return value