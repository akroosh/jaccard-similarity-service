from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from settings import DEBUG, POSTGRES_URL


engine = create_engine(POSTGRES_URL, echo=DEBUG, pool_pre_ping=True)
SessionLocal = sessionmaker(class_=Session, autocommit=False, autoflush=False, bind=engine)


class SQLAlchemySessionContextManager:
    def __init__(self):
        """Set up a database session for use in the rest of the functions."""
        self.session = SessionLocal()

    def __enter__(self):
        """Return the object that will be assigned to the variable in as clause of with statement."""
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the session."""
        self.session.close()
