from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from database import User
import uuid

# Create the SQLAlchemy engine

SQLALCHEMY_DATABASE_URL = "sqlite:////Users/mohanakarthikeyan/Documents/Mohan/Projects/e-commerce/user_service/test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
print(f"Using database URL: {SQLALCHEMY_DATABASE_URL}")

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_users():
    # Create a new session
    db = SessionLocal()
    try:
        print("Connecting to the database...")  # Debugging information

        # Check if the users table exists
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        print(f"Tables in the database: {table_names}")
        if 'users' not in table_names:
            print("The 'users' table does not exist.")
            return
        
        # Direct SQL query for debugging
        result = db.execute(text("SELECT * FROM users"))
        rows = result.fetchall()
        print(f"Number of rows retrieved using direct SQL: {len(rows)}")
        for row in rows:
            print(row)

        # Get the count of rows in the users table
        user_count = db.query(User).count()
        print(f"Number of users in the database: {user_count}")

        if user_count == 0:
            print("No users found in the database.")  # Debugging information
            return
        
        # Query all users
        users = db.query(User).all()

        # Print user details
        for user in users:
            user_id = uuid.UUID(bytes=user.user_id)  # Convert BLOB to UUID
            print(f"User ID: {user_id}, Email: {user.email}, Mobile: {user.mobile_number}, "
                  f"First Name: {user.first_name}, Last Name: {user.last_name}, Address: {user.address}, "
                  f"Created At: {user.created_at}, Updated At: {user.updated_at}")
    except Exception as e:
        print(f"An error occurred: {e}")  # Debugging information
    finally:
        # Close the session
        db.close()
        print("Database connection closed.")  # Debugging information

if __name__ == "__main__":
    get_users()
