from app.extensions import db

class PatientRecord(db.Model):
    __tablename__ = 'patient_records'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment_plan = db.Column(db.Text, nullable=False)
    date_of_visit = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    
    doctor = db.relationship('User', foreign_keys=[doctor_id])
    hospital = db.relationship('Hospital', back_populates='patient_records')
    
    record_patient = db.relationship(
        'User',
        foreign_keys=[patient_id],
        back_populates='patient_records'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'hospital_id': self.hospital_id,
            'diagnosis': self.diagnosis,
            'treatment_plan': self.treatment_plan,
            'date_of_visit': self.date_of_visit.isoformat()
        }