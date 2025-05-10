"""
Database configuration module using SQLAlchemy ORM.

This module sets up the database connection, session factory, and declarative base
for defining ORM models. It uses SQLite as the backend.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# SQLite database URL
DATABASE_URL = "sqlite:///./user.db"

# Create the SQLAlchemy engine with specific connection arguments
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite with multithreaded apps
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Base class for ORM models
Base = declarative_base()
