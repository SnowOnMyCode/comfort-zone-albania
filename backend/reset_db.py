from database import engine, Base
import models

Base.metadata.drop_all(bind=engine)   # Delete all tables
Base.metadata.create_all(bind=engine) # Recreate them
print("Done!")