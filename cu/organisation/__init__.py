"""
Interface between the app and the database for organisations
"""
from cu.database import db_session
from cu.database.models import Organisation


def create(name, user, description=None):
    """
    Creates a new Organisation
    :param name: String, name of the organisation
    :param user: User, user who created the organisation
    :param description: String, description of the organisation
    :return: int, id of the new organisation
    """
    print("creating...")
    o = Organisation(str(name), user, description)
    db_session.add(o)

    user.add_organisation(o)

    db_session.commit()

    return o.id


def get(id):
    """
    Gets an Organisation from it's id
    :param id: int
    :return: Organisation
    """
    o = Organisation.query.get(id)

    if o is None:
        raise ValueError("An organisation by that id doesn't exist")

    return o

def commit_changes():
    db_session.commit()