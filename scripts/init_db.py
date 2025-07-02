#!/usr/bin/env python3
"""
Database initialization script
"""
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.app.database import engine, Base
from backend.app.models import *


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def drop_tables():
    """Drop all database tables"""
    print("Dropping database tables...")
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped successfully!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        drop_tables()
    else:
        create_tables()