"""
Database models
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UnicodeText, Table, DateTime
from sqlalchemy.orm import relationship, backref
from cu.database import Base
from cu import util

# So users can follow organisations
user_org_follow_table = Table(
    'user_org_follow',
    Base.metadata,
    Column('organisation_id', Integer, ForeignKey('organisation.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)

# So users can follow events
user_event_follow_table = Table(
    'user_event_follow',
    Base.metadata,
    Column('event_id', Integer, ForeignKey('event.id')),
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

    organisations_following = relationship(
        'Organisation',
        secondary=user_org_follow_table,
        back_populates='followers'
    )

    events_following = relationship(
        'Event',
        secondary=user_event_follow_table,
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

    def follow_organisation(self, org):
        if org not in self.organisations_following:
            self.organisations_following.append(org)

    def unfollow_organisation(self, org):
        if org in self.organisations_following:
            self.organisations_following.remove(org)

    def follow_event(self, event):
        if event not in self.events_following:
            self.events_following.append(event)

    def unfollow_event(self, event):
        if event in self.events_following:
            self.events_following.remove(event)

    def transfer_organisation(self, new_manager):
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
        back_populates='organisations_following'
    )

    events = relationship('Event', back_populates='organisation')

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
        if u not in self.followers:
            self.followers.append(u)

    def rem_follower(self, u):
        if u in self.followers:
            self.followers.remove(u)

    def add_event(self, e):
        self.events.append(e)

    def rem_event(self, e):
        self.events.remove(e)


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    description = Column(UnicodeText)

    organisation_id = Column(Integer, ForeignKey('organisation.id'))
    organisation = relationship('Organisation', back_populates='events')

    followers = relationship(
        'User',
        secondary=user_event_follow_table,
        back_populates='events_following'
    )

    def __init__(self, title, datetime, location, decription=None):
        self.title = title
        self.datetime = datetime
        self.location = location
        self.description = decription
