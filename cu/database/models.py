"""
Database models
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UnicodeText
from sqlalchemy.orm import relationship, backref
from cu.database import Base
from cu import util


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    google_id = Column(String, unique=True, nullable=False)
    active = Column(Boolean, nullable=False)  # Defaults to True, can be set to False if user is banned

    organisation = relationship(
        'Organisation',
        backref="user",
        uselist=False
    )

    def __init__(self, google_id, name=None, active=True):
        self.google_id = google_id
        self.name = name
        self.active = active

    def add_organisation(self, org):
        self.organisation = org

    def rem_organisation(self):
        self.organisation = None

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
        return '<User %r: %r>' % (self.id, self.name)


class Organisation(Base):
    __tablename__ = 'organisation'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url_name = Column(String, nullable=False)
    description = Column(UnicodeText)

    manager = Column(Integer, ForeignKey(User.id))

    def __init__(self, name=None, manager=None, description=None):
        self.name = name
        self.url_name = util.urlify_string(name)
        self.manager = manager
        self.description = description
