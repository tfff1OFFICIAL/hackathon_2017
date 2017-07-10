"""
Database models
"""
import bcrypt
from sqlalchemy import Column, Integer, String, Text
from cu.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def __init__(self, username=None, email=None):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r: %r>' % (self.id, self.username)


class Organisation(Base):
    __tablename__ = "organisations"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(Text)

    def verify_password(self, attempted):
        pwhash = bcrypt.hashpw(attempted, self.password)
        return self.password == pwhash
