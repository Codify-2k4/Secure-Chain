from app import create_app, db
from app.models import User, Patient, AccessPermission

app = create_app()

def cleanup_database():
    """Clean up existing data and standardize passwords"""
    print("\nStarting database cleanup...")
    with app.app_context():
        try:
            # Standardize all passwords
            users = User.query.all()
            for user in users:
                if user.role == 'admin':
                    user.set_password('admin123')
                elif user.role == 'doctor':
                    user.set_password('doctor123')
                elif user.role == 'patient':
                    user.set_password('patient123')
                print(f"Updated password for {user.username} ({user.role})")
            
            db.session.commit()

            # Remove duplicate patients (patient01, patient02)
            # First find and delete the patient records
            old_patients = User.query.filter(User.username.in_(['patient01', 'patient02'])).all()
            for old_patient in old_patients:
                # First delete the associated patient record if it exists
                patient_record = Patient.query.filter_by(user_id=old_patient.id).first()
                if patient_record:
                    db.session.delete(patient_record)
                    db.session.commit()
                
                # Then delete the user
                print(f"Removing duplicate patient: {old_patient.username}")
                db.session.delete(old_patient)
                db.session.commit()
            
            print("Database cleanup completed successfully!")
            return True
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
            db.session.rollback()
            return False

def seed_database():
    """Seed the database with initial data"""
    print("\nStarting database seeding...")
    with app.app_context():
        try:
            db.create_all()

            # Admin User
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(username='admin', role='admin')
                db.session.add(admin)
                print("Created admin user")
            admin.set_password('admin123')

            # Doctors
            doctors = [
                {'username': 'dr_smith', 'role': 'doctor'},
                {'username': 'dr_jones', 'role': 'doctor'},
            ]
            for doc in doctors:
                doctor = User.query.filter_by(username=doc['username']).first()
                if not doctor:
                    doctor = User(username=doc['username'], role=doc['role'])
                    db.session.add(doctor)
                    print(f"Created doctor: {doc['username']}")
                doctor.set_password('doctor123')

            db.session.commit()

            # Patients
            patients_data = [
                {'username': 'patient1', 'name': 'John Doe', 'age': 35, 
                 'disease': 'Diabetes', 'doctor_username': 'dr_smith'},
                {'username': 'patient2', 'name': 'Jane Smith', 'age': 28,
                 'disease': 'Hypertension', 'doctor_username': 'dr_jones'},
            ]
            
            for data in patients_data:
                user = User.query.filter_by(username=data['username']).first()
                if not user:
                    user = User(username=data['username'], role='patient')
                    db.session.add(user)
                    print(f"Created patient user: {data['username']}")
                user.set_password('patient123')
                db.session.flush()
                
                doctor = User.query.filter_by(username=data['doctor_username']).first()
                patient = Patient.query.filter_by(user_id=user.id).first()
                if not patient:
                    patient = Patient(
                        name=data['name'],
                        age=data['age'],
                        disease=data['disease'],
                        user_id=user.id,
                        doctor_id=doctor.id if doctor else None
                    )
                    db.session.add(patient)
                    print(f"Created patient record: {data['name']}")

            db.session.commit()

            # Access Permissions
            access_permissions = [
                {'doctor_username': 'dr_smith', 'patient_username': 'patient1', 'granted': True},
                {'doctor_username': 'dr_jones', 'patient_username': 'patient2', 'granted': True},
            ]
            
            for perm in access_permissions:
                doctor = User.query.filter_by(username=perm['doctor_username']).first()
                patient_user = User.query.filter_by(username=perm['patient_username']).first()
                patient = Patient.query.filter_by(user_id=patient_user.id).first() if patient_user else None
                
                if doctor and patient:
                    access = AccessPermission.query.filter_by(
                        doctor_id=doctor.id,
                        patient_id=patient.id
                    ).first()
                    
                    if not access:
                        access = AccessPermission(
                            doctor_id=doctor.id,
                            patient_id=patient.id,
                            granted=perm['granted']
                        )
                        db.session.add(access)
                        print(f"Created access permission for Dr. {doctor.username} to {patient.name}")

            db.session.commit()
            print("Database seeding completed successfully!")
            return True
        except Exception as e:
            print(f"Error during seeding: {str(e)}")
            db.session.rollback()
            return False

def initialize_database():
    """Main function to clean and seed the database"""
    print("Starting database initialization...")
    
    # First perform cleanup
    if not cleanup_database():
        print("Aborting due to cleanup errors")
        return False
    
    # Then perform seeding
    if not seed_database():
        print("Aborting due to seeding errors")
        return False
    
    print("\nDatabase initialization completed successfully!")
    return True

if __name__ == '__main__':
    with app.app_context():
        initialize_database()