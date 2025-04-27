# reset_passwords.py
from app import create_app, db
from app.models import User

app = create_app()

def reset_all_passwords():
    with app.app_context():
        try:
            # Reset admin password
            admin = User.query.filter_by(username='admin').first()
            if admin:
                admin.set_password('admin123')
                print(f"Reset password for admin")

            # Reset all doctors
            doctors = User.query.filter_by(role='doctor').all()
            for doctor in doctors:
                doctor.set_password('doctor123')
                print(f"Reset password for doctor {doctor.username}")

            # Reset all patients
            patients = User.query.filter_by(role='patient').all()
            for patient in patients:
                patient.set_password('patient123')
                print(f"Reset password for patient {patient.username}")

            db.session.commit()
            print("All passwords reset successfully!")
        except Exception as e:
            print(f"Error resetting passwords: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    reset_all_passwords()