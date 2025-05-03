from datetime import datetime
from sqlalchemy.orm import validates
from app.extensions import db

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    patient_user = db.relationship(
        'User', 
        foreign_keys=[patient_id],
        back_populates='patient_appointments'
    )
    
    doctor_user = db.relationship(
        'User',
        foreign_keys=[doctor_id],
        back_populates='doctor_appointments'
    )
    
    hospital = db.relationship(
        'Hospital',
        back_populates='appointments'
    )

    # Correct decorator usage
    @validates('appointment_date')
    def validate_appointment_date(self, key, value):
        """Validation logic for appointment date"""
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Invalid ISO date format. Use: YYYY-MM-DDTHH:MM:SS")
        
        if value < datetime.now():
            raise ValueError("Appointment date cannot be in the past")
        
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'hospital_id': self.hospital_id,
            'appointment_date': self.appointment_date.isoformat(),
            'purpose': self.purpose,
            'status': self.status
        }