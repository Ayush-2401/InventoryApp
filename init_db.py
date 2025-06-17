# init_db.py
from utils import engine
from models import Base, Operator # Import Operator to ensure it's loaded for Base.metadata.create_all
import os

# Define the path to your SQLite database file
db_path = './inventory.db'

# Optional: Delete existing database file if it exists, for a clean start
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed existing database: {db_path}")

# Create all tables defined in Base's metadata
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")

# Optionally, insert default data
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Insert a default operator for testing
    # Using merge to prevent duplicates if script is run multiple times
    admin_user = Operator(username='admin', password='adminpass')
    user_user = Operator(username='user', password='userpass')

    session.merge(admin_user)
    session.merge(user_user)
    session.commit()
    print("Default operators (admin, user) ensured in database.")
except Exception as e:
    session.rollback()
    print(f"Error inserting default operators: {e}")
finally:
    session.close()