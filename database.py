"""
Database setup and initialization
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def init_db():
    """Initialize database tables"""
    db.create_all()

def reset_db():
    """Reset all database tables (use with caution)"""
    db.drop_all()
    db.create_all()