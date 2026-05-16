"""
Database models for the notes service
"""

from database import db
from datetime import datetime
import uuid

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    notes = db.relationship('Note', backref='author', lazy=True, cascade='all, delete-orphan')
    shared_notes = db.relationship('SharedNote', backref='shared_with_user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class Note(db.Model):
    """Note model"""
    __tablename__ = 'notes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    shared_with = db.relationship('SharedNote', backref='note', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Note {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class SharedNote(db.Model):
    """Model for tracking shared notes"""
    __tablename__ = 'shared_notes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    note_id = db.Column(db.String(36), db.ForeignKey('notes.id'), nullable=False, index=True)
    shared_with_user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    shared_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate shares
    __table_args__ = (db.UniqueConstraint('note_id', 'shared_with_user_id', name='unique_note_share'),)
    
    def __repr__(self):
        return f'<SharedNote note={self.note_id} with={self.shared_with_user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'note_id': self.note_id,
            'shared_with_user_id': self.shared_with_user_id,
            'shared_at': self.shared_at.isoformat()
        }