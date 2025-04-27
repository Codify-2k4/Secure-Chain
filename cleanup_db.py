from app import create_app, db
from app.models import User, Patient

app = create_app()

def cleanup_database():
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
            
            # Remove duplicate patients
            old_patients = User.query.filter(User.username.in_(['patient01', 'patient02'])).all()
            for old_patient in old_patients:
                db.session.delete(old_patient)
            
            db.session.commit()
            print("Database cleaned up and passwords standardized!")
        except Exception as e:
            print(f"Error cleaning database: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    cleanup_database()