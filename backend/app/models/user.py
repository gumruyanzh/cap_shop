from datetime import datetime
from app import db, bcrypt


class User(db.Model):
    """User model for authentication and customer data"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, username, email, password, first_name=None, last_name=None):
        """Initialize user with hashed password"""
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password):
        """Check if provided password matches the hash"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        """Convert user object to dictionary (exclude sensitive data)"""
        user_dict = {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_email:
            user_dict['email'] = self.email
        return user_dict

    def __repr__(self):
        return f'<User {self.username}>'
