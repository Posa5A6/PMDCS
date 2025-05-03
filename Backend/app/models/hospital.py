from app.extensions import db

class Hospital(db.Model):
    __tablename__ = 'hospitals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)

    # Relationships
    doctors = db.relationship('User', back_populates='hospital', lazy='dynamic')
    appointments = db.relationship('Appointment', back_populates='hospital')
    patient_records = db.relationship('PatientRecord', back_populates='hospital')
    authorized_doctors = db.relationship('DoctorPermission', back_populates='hospital')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }