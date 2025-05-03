from app.extensions import db
from sqlalchemy.orm import validates

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id', ondelete='SET NULL'))


    # Relationships
    permissions = db.relationship('DoctorPermission', back_populates='doctor')
    hospital = db.relationship('Hospital', back_populates='doctors')
    patient_appointments = db.relationship(
        'Appointment', 
        foreign_keys='Appointment.patient_id',
        back_populates='patient_user',  # Changed from 'patient'
        lazy='dynamic'
    )
    
    doctor_appointments = db.relationship(
        'Appointment',
        foreign_keys='Appointment.doctor_id',
        back_populates='doctor_user',  # Changed from 'doctor'
        lazy='dynamic'
    )
    
    patient_records = db.relationship(
        'PatientRecord',
        foreign_keys='PatientRecord.patient_id',
        back_populates='record_patient',  # Changed from 'patient'
        lazy='dynamic'
    )

    @validates('role')
    def validate_role(self, key, value):
        roles = ['admin', 'doctor', 'patient']
        if value not in roles:
            raise ValueError(f"Role must be one of: {', '.join(roles)}")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
        }