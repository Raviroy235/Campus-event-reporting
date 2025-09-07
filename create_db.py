from app.database import Base, engine
import app.models as models

def create():
    Base.metadata.create_all(bind=engine)
    print("Database & tables created (events.db)")

if __name__ == "__main__":
    create()
