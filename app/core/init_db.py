# app/core/init_db.py
from app.core.database import Base, engine
from app.models.user import User


def init_db():
    """
    Create all database tables
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    init_db()
