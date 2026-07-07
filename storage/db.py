from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

def init_db():
    import storage.schemas
    Base.metadata.create_all(engine)

def get_session():
    return SessionLocal()
