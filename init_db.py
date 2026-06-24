from database import engine, SessionLocal, Base
from models import User

# Build the tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Check if admin already exists
existing_user = db.query(User).filter(User.user_name == "admin").first()

if not existing_user:
    # Create the dummy user
    dummy_user = User(
        user_name="admin",
        user_email_id="admin@example.com",
        user_status="active",
        password_hash="password123"
    )
    db.add(dummy_user)
    db.commit()
    print("Database built and admin user injected!")
else:
    print("Database already set up.")

db.close()
