"""
Database models
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from cu.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    google_id = Column(String, unique=True, nullable=False)
    active = Column(Boolean, nullable=False)  # Defaults to True, can be set to False if user is banned

    organisation = relationship(
        "Organisation",
        uselist=False,
        back_populates="manager"
    )

    def __init__(self, google_id, name=None, active=True):
        self.google_id = google_id
        self.name = name
        self.active = active

    def add_organisation(self, org):
        pass

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

    def ban(self):
        self.active = False

    def unban(self):
        self.active = True

    def __repr__(self):
        return '<User %r: %r>' % (self.id, self.username)


class Organisation(Base):
    __tablename__ = "organisations"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    manager_id = Column(Integer, ForeignKey('users.id'))
    manager = relationship("User", back_populates="organisation")

    def __init__(self, name):
        self.name = name