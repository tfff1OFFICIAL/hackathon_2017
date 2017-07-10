"""
Database models
"""
import bcrypt
import base64
import hashlib
from sqlalchemy import Column, Integer, String, Text, Boolean
from cu.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False)

    def __init__(self, username=None, email=None, password=''):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(
            base64.b64encode(
                hashlib.sha256(password.encode()).digest()  # To handle exceedingly long passwords
            ),
            bcrypt.gensalt()
        )
        self.active = True

    def verify_password(self, attempted):
        pwhash = bcrypt.hashpw(attempted, self.password)
        return self.password == pwhash

    def __repr__(self):
        return '<User %r: %r>' % (self.id, self.username)


class Organisation(Base):
    __tablename__ = "organisations"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(Text, nullable=False)

    def __init__(self, name=None, password=''):
        """
        :param password: Unicode String, the users unencrypted password
        """
        self.name = name
        self.password = bcrypt.hashpw(
            base64.b64encode(
                hashlib.sha256(password.encode()).digest()  # To handle exceedingly long passwords
            ),
            bcrypt.gensalt()
        )

    def verify_password(self, attempted):
        return bcrypt.checkpw(attempted, self.password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<Organisation %r: %r>' % (self.id, self.name)
