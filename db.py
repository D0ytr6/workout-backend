from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://user:1234@localhost/workoutDB"

# SqlAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# create session for operation with db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for models 
Base = declarative_base()
