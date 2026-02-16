from database import engine, Base
import models  # IMPORTANT: loads table definitions

# Create all tables
Base.metadata.create_all(bind=engine)

print("Database initialized successfully.")