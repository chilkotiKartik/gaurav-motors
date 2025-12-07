from hms.app import app, db, User, DoctorProfile, PatientProfile, Department, Availability
import os


def init_db():
    # remove existing DB during development to ensure schema is fresh
    db_path = os.path.join(os.path.dirname(__file__), 'hms.db')
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print('Removed existing hms.db to recreate schema')
        except Exception as e:
            print('Could not remove existing DB:', e)
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com', role='admin')
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print('Admin user created: username=admin password=admin')
        else:
            print('Admin already exists')

        # create sample department and doctor
        if not Department.query.filter_by(name='General').first():
            dept = Department(name='General', description='General Medicine')
            db.session.add(dept)
            db.session.commit()
        else:
            dept = Department.query.filter_by(name='General').first()

        if not User.query.filter_by(username='drjohn').first():
            u = User(username='drjohn', email='drjohn@example.com', role='doctor')
            u.set_password('doctor')
            db.session.add(u)
            db.session.commit()
            doc = DoctorProfile(user_id=u.id, name='Dr John Doe', specialization='General', availability='Mon-Fri 10:00-16:00')
            db.session.add(doc)
            db.session.commit()
            print('Sample doctor created: drjohn / doctor')
            # create some sample availability slots for next 7 days
            from datetime import datetime, timedelta
            today = datetime.utcnow().date()
            for i in range(7):
                date = today + timedelta(days=i)
                # add two slots per day
                from datetime import time as dtime
                s1 = Availability(doctor_id=doc.id, date=date, time=dtime(10,0), is_available=True)
                s2 = Availability(doctor_id=doc.id, date=date, time=dtime(15,0), is_available=True)
                db.session.add(s1)
                db.session.add(s2)
            db.session.commit()
        else:
            print('Sample doctor exists')

        print('Database initialized')


if __name__ == '__main__':
    init_db()
