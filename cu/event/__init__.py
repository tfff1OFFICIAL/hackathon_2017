"""
Interface between the app and the database for events
"""
from datetime import datetime
from cu.database import db_session
from cu.database.models import Event


def create(org, title, datetime, location, description=None):
    """
    Creates an Event and links it to org
    :param org: Organisation
    :param title: String
    :param datetime: DateTime
    :param location: String
    :param description: String
    :return: int, id of the new Event
    """
    e = Event(
        title,
        datetime,
        location,
        description
    )

    org.add_event(e)

    db_session.add(e)
    db_session.commit()

    return e.id


def get(id):
    """
    Gets an Event from it's id
    :param id: int
    :return: Event
    """
    e = Event.query.get(id)

    if e is None:
        raise ValueError("An event by that id doesn't exist")

    return e


def list_events(org=None):
    if org is None:
        events = db_session.query(Event.id)\
            .filter(Event.datetime >= datetime.now())\
            .order_by(Event.datetime.asc())
    else:
        events = db_session.query(Event.id) \
            .filter(Event.datetime >= datetime.now()) \
            .filter(Event.organisation_id == org) \
            .order_by(Event.datetime.asc())

    return events.all()


def list_past_events(org=None):
    if org is None:
        events = db_session.query(Event.id)\
            .filter(Event.datetime < datetime.now())\
            .order_by(Event.datetime.asc())
    else:
        events = db_session.query(Event.id)\
            .filter(Event.datetime < datetime.now())\
            .filter(Event.organisation_id == org)\
            .order_by(Event.datetime.asc())

    return events.all()


def commit_changes():
    db_session.commit()