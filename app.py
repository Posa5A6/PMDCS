from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,TextAreaField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_migrate import Migrate
from config import Config
from datetime import datetime, date
from sqlalchemy import func
import psycopg2

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # Initialize Bcrypt
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
migrate = Migrate(app, db)

# Define role constants for consistency
ROLE_ADMIN = 'admin'
ROLE_DOCTOR = 'doctor'
ROLE_PATIENT = 'patient'





# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # admin, doctor, patient

    # Foreign key for doctors belonging to a hospital
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
    hospital = db.relationship('Hospital', backref='doctors')

    def __repr__(self):
        return f'<User {self.username} - {self.role}>'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class PatientRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_name = db.Column(db.String(150), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    hospital = db.relationship('Hospital', backref='patient_records')
    diagnosis = db.Column(db.String(255), nullable=False)
    treatment_plan = db.Column(db.Text, nullable=False)
    date_of_visit = db.Column(db.Date, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship to access patient data
    patient = db.relationship('User', foreign_keys=[patient_id])
    #doctor = db.relationship('User', foreign_keys=[doctor_name])

# Registration form class
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[(ROLE_ADMIN, 'Admin'), (ROLE_DOCTOR, 'Doctor'), (ROLE_PATIENT, 'Patient')],
                       validators=[DataRequired()])
    submit = SubmitField('Sign Up')


# Login form class
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


# Patient record form class (Updated with hospital details)
# Patient record form class (Updated to use hospital_id instead of hospital_name)
class PatientRecordForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    doctor_name = StringField('Doctor Name', validators=[DataRequired()])
    hospital_id = SelectField('Hospital', coerce=int, validators=[DataRequired()])  # Use hospital_id here
    diagnosis = StringField('Diagnosis', validators=[DataRequired()])
    treatment_plan = TextAreaField('Treatment Plan', validators=[DataRequired()])
    date_of_visit = DateField('Date of Visit', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Save Record')



class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_name = db.Column(db.String(150), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)  # Add this line
    appointment_date = db.Column(db.Date, nullable=False)
    purpose_of_appointment = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    email = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)

    # Relationships
    patient = db.relationship('User', backref='appointments')
    hospital = db.relationship('Hospital', backref='appointments')  # Add this line for the relationship







# AppointmentForm (Updated with all required fields)
class AppointmentForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    hospital_id = SelectField('Hospital', coerce=int, validators=[DataRequired()])
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    purpose_of_appointment = StringField('Purpose of Appointment', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    blood_group = StringField('Blood Group', validators=[DataRequired()])
    appointment_date = DateField('Appointment Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.hospital_id.choices = [(hospital.id, hospital.name) for hospital in Hospital.query.all()]
        self.doctor_id.choices = [(doctor.id, doctor.username) for doctor in User.query.filter_by(role=ROLE_DOCTOR).all()]



# UpdateInfoForm (Updated with required fields for personal info update)
class UpdatePersonalInfoForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    blood_group = StringField('Blood Group', validators=[DataRequired()])
    password = PasswordField('Password')  # Password is optional
    submit = SubmitField('Update Information')


# ContactMessage Model
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<ContactMessage {self.name} - {self.subject}>"


class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=100)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Message')

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Hospital {self.name}>'

class HospitalForm(FlaskForm):
    name = StringField('Hospital Name', validators=[DataRequired(), Length(min=2, max=150)])
    address = StringField('Address', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Add Hospital')

class DoctorPermission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))

    doctor = db.relationship('User', backref='permissions')
    hospital = db.relationship('Hospital', backref='authorized_doctors')

class AssignPermissionForm(FlaskForm):
    doctor_id = SelectField('Doctor', coerce=int)
    hospital_id = SelectField('Hospital', coerce=int)
    submit = SubmitField('Assign Permission')

    def __init__(self, *args, **kwargs):
        super(AssignPermissionForm, self).__init__(*args, **kwargs)
        self.doctor_id.choices = [(doctor.id, doctor.username) for doctor in User.query.filter_by(role='doctor').all()]
        self.hospital_id.choices = [(hospital.id, hospital.name) for hospital in Hospital.query.all()]

class GrantPermissionForm(FlaskForm):
    doctor_id = SelectField('Doctor', coerce=int)
    hospital_id = SelectField('Hospital', coerce=int)
    submit = SubmitField('Grant Permission')

class EditRecordForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    doctor_name = StringField('Doctor Name', validators=[DataRequired()])
    hospital_id = SelectField('Hospital', coerce=int, validators=[DataRequired()])
    diagnosis = StringField('Diagnosis', validators=[DataRequired()])
    treatment_plan = TextAreaField('Treatment Plan', validators=[DataRequired()])
    date_of_visit = DateField('Date of Visit', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class CancelAppointmentForm(FlaskForm):
    submit = SubmitField('Cancel Appointment')


# Home route
@app.route('/')
def home():
    return render_template('home.html')


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) |
            (User.email == form.email.data)
        ).first()
        if existing_user:
            flash('Username or Email already exists. Please try again.', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Hash the password
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                role=form.role.data.lower()  # Store role in lowercase
            )
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # Verify hashed password
            login_user(user)
            print(f"Logged in user's role: {user.role}")  # Debugging statement
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your credentials and try again.', 'danger')
    return render_template('login.html', form=form)


# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    user_role = current_user.role.lower()
    print(f"Dashboard accessed by user with role: {current_user.role}")  # Debugging statement
    if user_role == ROLE_ADMIN:
        return redirect(url_for('admin_dashboard'))
    elif user_role == ROLE_DOCTOR:
        return redirect(url_for('doctor_dashboard'))
    elif user_role == ROLE_PATIENT:
        return redirect(url_for('patient_dashboard'))
    else:
        return redirect(url_for('home'))


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    user_role = current_user.role.lower()
    print(f"Admin Dashboard accessed by user with role: {current_user.role}")  # Debugging statement
    if user_role != ROLE_ADMIN:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))

    # Rest of your logic
    total_appointments = Appointment.query.count()
    total_patients = User.query.filter_by(role=ROLE_PATIENT).count()
    total_doctors = User.query.filter_by(role=ROLE_DOCTOR).count()

    return render_template('admin_dashboard.html',
                           total_appointments=total_appointments,
                           total_patients=total_patients,
                           total_doctors=total_doctors)


# User Management Route (view all users)
@app.route('/manage_users')
@login_required
def manage_users():
    user_role = current_user.role.lower()
    print(f"Manage Users accessed by user with role: {current_user.role}")  # Debugging statement
    if user_role != ROLE_ADMIN:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))

    users = User.query.all()  # Fetch all users from the database
    return render_template('user_management.html', users=users)


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    user_role = current_user.role.lower()
    print(f"Add User accessed by user with role: {current_user.role}")  # Debugging statement
    if user_role != ROLE_ADMIN:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))

    form = RegistrationForm()  # Reusing the registration form for adding users

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('add_user'))

        # Create the new user with hashed password and role in lowercase
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Hash the password
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data.lower()
        )
        db.session.add(user)
        db.session.commit()
        flash('User added successfully', 'success')
        return redirect(url_for('manage_users'))

    return render_template('add_user.html', form=form)


# Edit User Route
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user_role = current_user.role.lower()
    print(f"Edit User accessed by user with role: {current_user.role}")  # Debugging statement
    if user_role != ROLE_ADMIN:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('manage_users'))

    # Populate the form with existing user data, except password
    form = RegistrationForm(obj=user)
    form.password.validators = []  # Remove validators for password if not changing
    form.confirm_password.validators = [EqualTo('password', message='Passwords must match.')]

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data.lower()
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Hash the new password
            user.password = hashed_password  # Update password if provided
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('manage_users'))

    return render_template('edit_user.html', form=form, user=user)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user_role = current_user.role.lower()
    print(f"Delete User accessed by user with role: {current_user.role}")  # Debugging statement
    if user_role != ROLE_ADMIN:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)

    # Check if the user has any appointments
    if Appointment.query.filter_by(patient_id=user.id).count() > 0:
        flash('Cannot delete user with active appointments. Please delete the appointments first.', 'danger')
        return redirect(url_for('manage_users'))

    db.session.delete(user)
    db.session.commit()

    flash('User deleted successfully', 'success')
    return redirect(url_for('manage_users'))


@app.route('/admin_appointment_management', methods=['GET', 'POST'])
@login_required
def admin_appointment_management():
    user_role = current_user.role.lower()
    print(f"Admin Appointment Management accessed by user with role: {current_user.role}")  # Debugging statement
    if user_role != ROLE_ADMIN:
        flash("Unauthorized access to Admin dashboard!", "danger")
        return redirect(url_for('home'))

    # Fetch all appointments
    appointments = Appointment.query.all()

    return render_template('admin_appointment_management.html', appointments=appointments)


@app.route('/delete_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    user_role = current_user.role.lower()
    print(f"Delete Appointment accessed by user with role: {current_user.role}")  # Debugging statement
    appointment = Appointment.query.get_or_404(appointment_id)

    # Ensure only admin can delete appointments
    if user_role != ROLE_ADMIN:
        flash('You are not authorized to delete this appointment!', 'danger')
        return redirect(url_for('admin_appointment_management'))

    db.session.delete(appointment)
    db.session.commit()

    flash('Appointment deleted successfully!', 'success')
    return redirect(url_for('admin_appointment_management'))


@app.route('/admin_manage_records')
@login_required
def admin_manage_records():
    user_role = current_user.role.lower()
    print(f"user_role: '{user_role}', ROLE_ADMIN: '{ROLE_ADMIN}'")  # Debugging statement with quotes

    if user_role != ROLE_ADMIN:
        flash("Unauthorized access!", 'danger')
        return redirect(url_for('dashboard'))

    # Proceed with admin functionalities
    records = PatientRecord.query.all()
    return render_template('admin_manage_records.html', records=records)


# Patient view to manage their own medical history
@app.route('/patient_records')
@login_required
def patient_records():
    user_role = current_user.role.lower()
    print(f"Patient Records accessed by user with role: {current_user.role}")  # Debugging statement
    if user_role != ROLE_PATIENT:
        flash("Unauthorized access!", 'danger')
        return redirect(url_for('dashboard'))

    records = PatientRecord.query.filter_by(patient_id=current_user.id).all()  # Fetch patient-specific records
    return render_template('patient_records.html', records=records)


@app.route('/create_record', methods=['GET', 'POST'])
@login_required
def create_record():
    form = PatientRecordForm()

    # Populate choices for patient and hospital dropdowns
    form.patient_id.choices = [(patient.id, patient.username) for patient in User.query.filter_by(role=ROLE_PATIENT).all()]
    form.hospital_id.choices = [(hospital.id, hospital.name) for hospital in Hospital.query.all()]
    #form.doctor_name.choices = [(doctor.username)]

    if form.validate_on_submit():
        record = PatientRecord(
            patient_id=form.patient_id.data,
            doctor_name=form.doctor_name.data,
            hospital_id=form.hospital_id.data,  # Corrected to hospital_id from the form
            diagnosis=form.diagnosis.data,
            treatment_plan=form.treatment_plan.data,
            date_of_visit=form.date_of_visit.data
        )
        db.session.add(record)
        db.session.commit()
        flash('Patient record added successfully!', 'success')
        return redirect(url_for('admin_manage_records'))

    # Ensure that hospitals are sent to the template for the dropdown
    hospitals = Hospital.query.all()
    return render_template('create_record.html', form=form, hospitals=hospitals)


@app.route('/edit_record/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    record = PatientRecord.query.get_or_404(record_id)
    form = PatientRecordForm(obj=record)

    # Fetch all hospitals and patients to populate the dropdowns
    hospitals = Hospital.query.all()
    patients = User.query.filter_by(role='patient').all()

    # Set the patient_id and hospital_id choices
    form.patient_id.choices = [(patient.id, patient.username) for patient in patients]
    form.hospital_id.choices = [(hospital.id, hospital.name) for hospital in hospitals]

    if form.validate_on_submit():
        # If form is submitted, update the record with new values
        record.patient_id = form.patient_id.data
        record.doctor_name = form.doctor_name.data
        record.hospital_id = form.hospital_id.data
        record.diagnosis = form.diagnosis.data
        record.treatment_plan = form.treatment_plan.data
        record.date_of_visit = form.date_of_visit.data

        db.session.commit()
        flash('Record updated successfully!', 'success')
        return redirect(url_for('admin_manage_records'))

    # Render the form again for editing
    return render_template('edit_record.html', form=form, record=record, hospitals=hospitals)

@app.route('/update_record/<int:record_id>', methods=['GET', 'POST'])
@login_required
def update_record(record_id):
    record = PatientRecord.query.get_or_404(record_id)
    form = EditRecordForm(obj=record)

    # Populate choices for the SelectFields
    form.patient_id.choices = [(patient.id, patient.username) for patient in User.query.filter_by(role='patient').all()]
    form.hospital_id.choices = [(hospital.id, hospital.name) for hospital in Hospital.query.all()]

    if form.validate_on_submit():
        # Update record with form data
        form.populate_obj(record)
        db.session.commit()
        flash('Record updated successfully!', 'success')
        return redirect(url_for('doctor_dashboard'))

    return render_template('edit_record.html', form=form, record=record)


@app.route('/delete_record/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    user_role = current_user.role.lower()

    if user_role != ROLE_ADMIN:
        flash("Unauthorized access!", 'danger')
        return redirect(url_for('dashboard'))

    # Fetch the record by its ID
    record = PatientRecord.query.get_or_404(record_id)

    # Proceed to delete the record
    db.session.delete(record)
    db.session.commit()

    flash("Patient record deleted successfully!", 'success')
    return redirect(url_for('admin_manage_records'))




@app.route('/admin/assign_permission', methods=['GET', 'POST'])
@login_required
def assign_permission():
    if current_user.is_admin:  # Only admins can assign permissions
        form = AssignPermissionForm()  # A form where you can choose doctor and hospital
        if form.validate_on_submit():
            doctor_id = form.doctor_id.data
            hospital_id = form.hospital_id.data

            # Create new permission
            permission = DoctorPermission(doctor_id=doctor_id, hospital_id=hospital_id)
            db.session.add(permission)
            db.session.commit()

            flash('Permission assigned successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('assign_permission.html', form=form)
    else:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('index'))


@app.route('/grant_permission', methods=['GET', 'POST'])
@login_required
def grant_permission():
    if current_user.role.lower() != ROLE_ADMIN:
        flash("Unauthorized access!", 'danger')
        return redirect(url_for('home'))

    form = GrantPermissionForm()

    # Populate doctor and hospital choices
    form.doctor_id.choices = [(doctor.id, doctor.username) for doctor in User.query.filter_by(role=ROLE_DOCTOR).all()]
    form.hospital_id.choices = [(hospital.id, hospital.name) for hospital in Hospital.query.all()]

    if form.validate_on_submit():
        doctor_id = form.doctor_id.data
        hospital_id = form.hospital_id.data

        # Check if permission already exists
        existing_permission = DoctorPermission.query.filter_by(doctor_id=doctor_id, hospital_id=hospital_id).first()
        if existing_permission:
            flash('Permission already exists for this doctor and hospital.', 'warning')
        else:
            # Grant permission
            permission = DoctorPermission(doctor_id=doctor_id, hospital_id=hospital_id)
            db.session.add(permission)
            db.session.commit()
            flash('Permission granted successfully!', 'success')

        return redirect(url_for('admin_dashboard'))

    return render_template('grant_permission.html', form=form)

# Route to manage doctor permissions (admin view)
@app.route('/manage_doctor_permissions', methods=['GET', 'POST'])
@login_required
def manage_doctor_permissions():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('admin_dashboard'))

    # Fetch all doctors and hospitals
    doctors = User.query.filter_by(role='doctor').all()
    hospitals = Hospital.query.all()

    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        hospital_id = request.form.get('hospital_id')

        # Add permission for doctor to access hospital
        if doctor_id and hospital_id:
            permission = DoctorPermission(doctor_id=doctor_id, hospital_id=hospital_id)
            db.session.add(permission)
            db.session.commit()
            flash('Permission granted successfully', 'success')

    # Fetch all existing permissions
    permissions = DoctorPermission.query.all()

    return render_template('manage_doctor_permissions.html', doctors=doctors, hospitals=hospitals, permissions=permissions)

# Route to revoke a doctor's permission
@app.route('/revoke_permission/<int:permission_id>', methods=['POST'])
@login_required
def revoke_permission(permission_id):
    permission = DoctorPermission.query.get(permission_id)
    if permission:
        db.session.delete(permission)
        db.session.commit()
        flash('Permission revoked successfully', 'success')
    return redirect(url_for('manage_doctor_permissions'))



#Doctor Dashboard Endpoints

@app.route('/doctor_dashboard', methods=['GET', 'POST'])
@login_required
def doctor_dashboard():
    user_role = current_user.role.lower()
    if user_role != ROLE_DOCTOR:
        flash("Unauthorized access!", 'danger')
        return redirect(url_for('home'))

    # Fetch hospitals doctor has permission to access
    doctor_permissions = DoctorPermission.query.filter_by(doctor_id=current_user.id).all()
    allowed_hospital_ids = [permission.hospital_id for permission in doctor_permissions]

    # Fetch hospitals and users (patients)
    hospitals = db.session.query(Hospital).filter(Hospital.id.in_(allowed_hospital_ids)).all()
    all_patients = db.session.query(User).all()

    # Fetch filters from the form
    selected_hospital = request.args.get('hospital')
    selected_username = request.args.get('username')

    # Filter patients based on hospital and/or username
    query = db.session.query(User, Hospital).join(PatientRecord, User.id == PatientRecord.patient_id) \
            .join(Hospital, Hospital.id == PatientRecord.hospital_id) \
            .filter(PatientRecord.doctor_name == current_user.username)

    if selected_hospital and selected_hospital != 'all':
        query = query.filter(PatientRecord.hospital_id == selected_hospital)

    if selected_username:
        query = query.filter(User.username.ilike(f"%{selected_username}%"))

    patients = query.all()

    # Fetch doctor's appointments
    appointments = Appointment.query.filter_by(doctor_name=current_user.username).all()

    # Add current time to context for checking expired appointments
    current_time = datetime.now().date()

    # Create a form for canceling appointments
    form = CancelAppointmentForm()

    return render_template(
        'doctor_dashboard.html',
        patients=patients,
        hospitals=hospitals,
        appointments=appointments,
        selected_hospital=selected_hospital,
        selected_username=selected_username,
        current_time=current_time,
        form=form,
        doctor_name=current_user.username  # Pass the doctor's name to the template
    )

@app.route('/doctor_manage_records/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def doctor_manage_records(patient_id):
    user_role = current_user.role.lower()
    if user_role != ROLE_DOCTOR:
        flash("Unauthorized access!", 'danger')
        return redirect(url_for('dashboard'))

    # Fetch the doctor's hospital permissions
    doctor_hospital_ids = [perm.hospital_id for perm in current_user.permissions]

    # Fetch patient's records
    records = PatientRecord.query.filter_by(patient_id=patient_id).all()

    # Restrict access based on hospital permissions
    if not any(record.hospital_id in doctor_hospital_ids for record in records):
        flash("You don't have permission to view or edit this patient's records from another hospital.", "danger")
        return redirect(url_for('doctor_dashboard'))

    return render_template('doctor_manage_records.html', records=records, patient_id=patient_id)


@app.route('/doctor_appointments')
@login_required
def doctor_appointments():
    user_role = current_user.role.lower()
    print(f"Doctor Appointments accessed by user with role: {current_user.role}")  # Debugging statement
    if user_role != ROLE_DOCTOR:
        flash("Unauthorized access to manage appointments!", "danger")
        return redirect(url_for('dashboard'))

    # Fetch appointments for the logged-in doctor
    appointments = Appointment.query.filter_by(doctor_name=current_user.username).all()

    return render_template('doctor_appointments.html', appointments=appointments)


@app.route('/doctor_edit_record/<int:record_id>', methods=['GET', 'POST'])
@login_required
def doctor_edit_record(record_id):
    record = PatientRecord.query.get_or_404(record_id)
    if current_user.role == 'doctor':
        # Check if the doctor has permission to edit records from this hospital
        if record.hospital_id not in [perm.hospital_id for perm in current_user.permissions]:
            flash('You do not have permission to edit records from this hospital.', 'danger')
            return redirect(url_for('doctor_dashboard'))

        # Proceed with editing logic
        form = EditRecordForm(obj=record)
        if form.validate_on_submit():
            # Update record
            form.populate_obj(record)
            db.session.commit()
            flash('Record updated successfully!', 'success')
            return redirect(url_for('doctor_dashboard'))
        return render_template('edit_record.html', form=form, record=record)
    else:
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('index'))


# Patient dashboard route
@app.route('/patient_dashboard')
@login_required
def patient_dashboard():
    user_role = current_user.role.lower()
    print(f"Patient Dashboard accessed by user with role: {current_user.role}")  # Debugging statement
    if user_role == ROLE_PATIENT:
        return render_template('patient_dashboard.html')
    else:
        flash("Unauthorized access to Patient dashboard!", "danger")
        return redirect(url_for('home'))


@app.route('/book_appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    user_role = current_user.role.lower()
    if user_role != ROLE_PATIENT:
        flash("Only patients can book an appointment.", 'danger')
        return redirect(url_for('dashboard'))

    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=current_user.id,
            doctor_name=User.query.get(form.doctor_id.data).username,
            hospital_id=form.hospital_id.data,
            appointment_date=form.appointment_date.data,
            purpose_of_appointment=form.purpose_of_appointment.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            address=form.address.data,
            age=int(form.age.data),
            gender=form.gender.data,
            blood_group=form.blood_group.data,
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('view_appointments'))
    return render_template('book_appointment.html', form=form)

@app.route('/approve_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def approve_appointment(appointment_id):
    user_role = current_user.role.lower()
    if user_role != ROLE_DOCTOR:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('dashboard'))

    appointment = Appointment.query.get_or_404(appointment_id)

    # Only allow the doctor assigned to approve the appointment
    if appointment.doctor_name != current_user.username:
        flash("You can only approve your own appointments.", "danger")
        return redirect(url_for('doctor_dashboard'))

    appointment.status = 'Approved'
    db.session.commit()

    flash('Appointment approved successfully!', 'success')
    return redirect(url_for('doctor_dashboard'))


@app.route('/view_appointments', methods=['GET'])
@login_required
def view_appointments():
    appointments = Appointment.query.filter_by(patient_id=current_user.id).all()
    current_time = datetime.now().date()  # Get current date

    # Loop through each appointment and update the status if the date is in the past
    for appointment in appointments:
        if appointment.appointment_date < current_time:
            if appointment.status != 'Completed':
                appointment.status = 'Completed'
                db.session.commit()  # Save the status update

    return render_template('view_appointments.html', appointments=appointments, current_time=current_time)


@app.route('/update_appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    user_role = current_user.role.lower()
    print(f"Update Appointment accessed by user with role: {current_user.role}")  # Debugging statement
    form = AppointmentForm()

    if user_role == ROLE_DOCTOR:
        # Doctors can only update their own appointments
        if appointment.doctor_name != current_user.username:
            flash("You can only update your own appointments.", "danger")
            return redirect(url_for('dashboard'))

    elif user_role == ROLE_ADMIN:
        pass  # Admins can update any appointment

    elif user_role == ROLE_PATIENT:
        # Patients can only update their own appointments
        if appointment.patient_id != current_user.id:
            flash("You can only update your own appointments.", "danger")
            return redirect(url_for('dashboard'))
    else:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('dashboard'))

    if form.validate_on_submit():
        # Update the appointment details
        appointment.appointment_date = form.appointment_date.data
        appointment.purpose_of_appointment = form.purpose_of_appointment.data
        appointment.doctor_name = form.doctor_name.data
        appointment.email = form.email.data
        appointment.phone_number = form.phone_number.data
        appointment.address = form.address.data
        appointment.age = int(form.age.data)  # Ensure age is stored as integer
        appointment.gender = form.gender.data
        appointment.blood_group = form.blood_group.data
        db.session.commit()

        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('view_appointments'))  # Redirect after updating the appointment

    elif request.method == 'POST':
        # Print form data and any errors to help debug
        print(form.data)  # Print submitted form data
        print(form.errors)  # Print any form validation errors

    elif request.method == 'GET':
        # Pre-fill the form with existing appointment data
        form.appointment_date.data = appointment.appointment_date
        form.purpose_of_appointment.data = appointment.purpose_of_appointment
        form.doctor_name.data = appointment.doctor_name
        form.email.data = appointment.email
        form.phone_number.data = appointment.phone_number
        form.address.data = appointment.address
        form.age.data = str(appointment.age)  # Convert integer to string for the form
        form.gender.data = appointment.gender
        form.blood_group.data = appointment.blood_group

    # Pass the appointment object to the template
    return render_template('update_appointment.html', form=form, appointment=appointment)


@app.route('/update_personal_info', methods=['GET', 'POST'])
@login_required
def update_personal_info():
    form = UpdatePersonalInfoForm()
    user_role = current_user.role.lower()
    print(f"Update Personal Info accessed by user with role: {current_user.role}")  # Debugging statement
    if user_role != ROLE_PATIENT:
        flash("Unauthorized access to update personal information!", "danger")
        return redirect(url_for('dashboard'))

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        appointment = Appointment.query.filter_by(patient_id=current_user.id).first()
        if appointment:
            appointment.phone_number = form.phone_number.data
            appointment.address = form.address.data
            appointment.age = int(form.age.data)  # Ensure age is stored as integer
            appointment.gender = form.gender.data
            appointment.blood_group = form.blood_group.data
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Hash the new password
            current_user.password = hashed_password  # Update password if provided
        db.session.commit()
        flash('Your information has been updated!', 'success')
        return redirect(url_for('patient_dashboard'))

    # Pre-fill form fields with current user data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        appointment = Appointment.query.filter_by(patient_id=current_user.id).first()
        if appointment:
            form.phone_number.data = appointment.phone_number
            form.address.data = appointment.address
            form.age.data = str(appointment.age)  # Convert integer to string for the form
            form.gender.data = appointment.gender
            form.blood_group.data = appointment.blood_group

    return render_template('update_personal_info.html', form=form)

from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField

# Define CancelAppointmentForm to include a hidden field
class CancelAppointmentForm(FlaskForm):
    appointment_id = HiddenField('appointment_id')
    submit = SubmitField('Cancel Appointment')


# Cancel Appointment route (Allows patients or doctors to cancel an appointment if it's before the appointment date)
@app.route('/cancel_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    user_role = current_user.role.lower()

    print(f"Cancel Appointment accessed by user with role: {current_user.role}")  # Debugging statement

    # Ensure the user is authorized to cancel the appointment
    if (user_role == ROLE_PATIENT and appointment.patient_id == current_user.id) or \
       (user_role == ROLE_DOCTOR and appointment.doctor_name == current_user.username):
        # Update the appointment status to "Cancelled"
        appointment.status = "Cancelled"
        db.session.commit()
        flash('Appointment cancelled successfully!', 'success')
    else:
        flash('Unauthorized action or appointment does not exist.', 'danger')

    # Redirect to the appropriate dashboard based on the user's role
    if user_role == ROLE_PATIENT:
        return redirect(url_for('view_appointments'))
    elif user_role == ROLE_DOCTOR:
        return redirect(url_for('doctor_dashboard'))


@app.route('/my_medical_history')
@login_required
def my_medical_history():
    user_role = current_user.role.lower()

    # Ensure only patients can access this route
    if user_role != ROLE_PATIENT:
        flash("Unauthorized access to view medical history!", "danger")
        return redirect(url_for('home'))

    # Query the patient's medical records based on the logged-in user's ID
    records = PatientRecord.query.filter_by(patient_id=current_user.id).all()

    # Render the template and pass the medical records to the template
    return render_template('my_medical_history.html', records=records)


@app.route('/appointment_management')
@login_required
def appointment_management():
    user_role = current_user.role.lower()
    print(f"Appointment Management accessed by user with role: {current_user.role}")  # Debugging statement
    if user_role != ROLE_ADMIN:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('appointment_management.html')  # Create this HTML file as a placeholder

@app.route('/add_hospital', methods=['GET', 'POST'])
@login_required
def add_hospital():
    if current_user.role != ROLE_ADMIN:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('dashboard'))

    form = HospitalForm()
    if form.validate_on_submit():  # Ensure the form validation is correctly being checked
        hospital = Hospital(name=form.name.data, address=form.address.data)
        db.session.add(hospital)
        db.session.commit()
        flash('Hospital added successfully!', 'success')
        return redirect(url_for('manage_hospitals'))

    return render_template('add_hospital.html', form=form)


@app.route('/manage_hospitals', methods=['GET'])
@login_required
def manage_hospitals():
    if current_user.role != ROLE_ADMIN:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('dashboard'))

    hospitals = Hospital.query.all()  # Fetch all hospitals from the database
    return render_template('manage_hospitals.html', hospitals=hospitals)


@app.route('/delete_hospital/<int:hospital_id>', methods=['POST'])
@login_required
def delete_hospital(hospital_id):
    if current_user.role != ROLE_ADMIN:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('dashboard'))

    hospital = Hospital.query.get_or_404(hospital_id)
    db.session.delete(hospital)
    db.session.commit()
    flash('Hospital deleted successfully!', 'success')
    return redirect(url_for('manage_hospitals'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact_message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(contact_message)
        db.session.commit()
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)


@app.route('/view_contact_messages')
@login_required
def view_contact_messages():
    user_role = current_user.role.lower()
    print(f"View Contact Messages accessed by user with role: {current_user.role}")  # Debugging statement
    if user_role not in [ROLE_ADMIN, ROLE_DOCTOR]:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))

    # Fetch all messages
    messages = ContactMessage.query.order_by(ContactMessage.timestamp.desc()).all()

    return render_template('view_contact_messages.html', messages=messages)


# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

