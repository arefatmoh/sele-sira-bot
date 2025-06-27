# sele_sira_bot/db/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """Database model for a user."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    profession = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    language = Column(String, default='en')
    role = Column(String, default='basic')
    joined_at = Column(DateTime, default=datetime.utcnow)


class Job(Base):
    """Database model for a job posting."""
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    employer_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    job_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    salary = Column(String, nullable=True)
    deadline = Column(String, nullable=True)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
