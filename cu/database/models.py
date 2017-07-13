"""
Database models
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UnicodeText, Table
from sqlalchemy.orm import relationship, backref
from cu.database import Base
from cu import util


user_org_follow_table = Table(
    'user_org_follow',
    Base.metadata,
    Column('organisation_id', Integer, ForeignKey('organisation.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)


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

    following = relationship(
        'Organisation',
        secondary=user_org_follow_table,
        back_populates='followers'
    )

    def __init__(self, google_id, name=None, active=True, display_name=None, about=None, location=None):
        self.google_id = google_id
        self.name = name
        self.active = active
        self.display_name = display_name
        self.about = about
        self.location = location

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

    def follow(self, org):
        self.following.append(org)

    def unfollow(self, org):
        self.following.remove(org)

    def transfer_manager(self, new_manager):
        """
        Transfers the managership of this organisation to a different User
        :param new_manager: User
        :return: None
        """
        o = self.organisation
        self.rem_organisation()

        new_manager.add_organisation(o)

    def __repr__(self):
        return '<User %r: %r>' % (self.id, self.name)


class Organisation(Base):
    __tablename__ = 'organisation'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url_name = Column(String, nullable=False)
    description = Column(UnicodeText)

    manager = Column(Integer, ForeignKey(User.id))

    followers = relationship(
        'User',
        secondary=user_org_follow_table,
        back_populates='following'
    )

    # Social Links
    facebook = Column(String)
    twitter = Column(String)
    youtube = Column(String)
    website = Column(String)
    email = Column(String)

    def __init__(
            self,
            name,
            manager=None,
            description=None,
            facebook=None,
            twitter=None,
            youtube=None,
            website=None,
            email=None
    ):
        self.name = name
        self.url_name = util.urlify_string(name)
        self.manager = manager
        self.description = description

        # Auto-subscribe the manager
        self.add_follower(self.manager)

        # Social Links
        self.facebook = facebook
        self.twitter = twitter
        self.youtube = youtube
        self.website = website
        self.email = email

    def add_follower(self, u):
        self.followers.append(u)

    def rem_follower(self, u):
        self.followers.remove(u)


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
