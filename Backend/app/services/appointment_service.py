from app.models import Appointment
from app.extensions import db
from datetime import datetime

class AppointmentService:
    @staticmethod
    def create_appointment(data):
        try:
            # Convert ISO string to datetime object
            data['appointment_date'] = datetime.fromisoformat(data['appointment_date'].replace('Z', '+00:00'))
            
            appointment = Appointment(**data)
            db.session.add(appointment)
            db.session.commit()
            return appointment.to_dict(), 201
        except ValueError as e:
            return {'message': f'Invalid date format: {str(e)}'}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500