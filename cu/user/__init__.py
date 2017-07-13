"""
Interface between the app and the database for users
"""
from cu.database import db_session
from cu.database.models import User


def create(google_id, name, active=True):
    """
    Create a new User instance and return it's id
    :param google_id:
    :param name:
    :param active: bool
    :return: int
    """
    u = User(
        google_id=google_id,
        name=name,
        active=active
    )
    db_session.add(u)
    db_session.commit()

    return u.id


def get(id):
    """
    Get a user by their id
    :param id: int
    :return: User
    """
    u = User.query.get(id)

    if u is None:
        raise ValueError("A user by that id doesn't exist")

    return u
