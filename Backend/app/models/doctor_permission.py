
from app.extensions import db

class DoctorPermission(db.Model):
    __tablename__ = 'doctor_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    
    doctor = db.relationship('User', back_populates='permissions')
    hospital = db.relationship('Hospital', back_populates='authorized_doctors')

    def to_dict(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'hospital_id': self.hospital_id
        }