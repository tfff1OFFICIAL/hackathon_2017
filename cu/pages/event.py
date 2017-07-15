"""
Event view functions
"""
import math
from flask import Blueprint, abort, redirect, render_template, request, jsonify
from flask_login import current_user, login_required
from cu import event
from .form import CreateEventForm


e = Blueprint(
    'event',
    __name__,
    template_folder='../template'
)


@e.route('/')
def index():
    return redirect('/')


@e.route('/<int:id>')
def view_event(id):
    """
    View event with id
    :param id: int
    """
    try:
        return render_template('event/view.shtml', event=event.get(id))
    except ValueError:
        abort(404)


@e.route('/add', methods=['POST', 'GET'])
@login_required
def add_event():
    if current_user.organisation:  # they do manage an organisation
        form = CreateEventForm(request.form)
        if request.method == 'POST' and form.validate():
            e = event.create(
                current_user.organisation,
                form.title.data,
                form.datetime.data,
                form.location.data,
                form.description.data
            )
            return redirect('/event/{}'.format(e))
        return render_template('event/add.shtml', form=form)
    else:
        abort(403)


@e.route('/<int:id>/follow', methods=['POST', 'GET'])
@login_required
def add_follower(id):
    """
    Adds the current user as a follower of event id
    :param id: int, the id of the current event
    """
    try:
        current_user.follow_event(event.get(id))
        event.commit_changes()
    except ValueError:
        abort(404)


@e.route('/<int:id>.json')
def api_eventdata(id):
    try:
        e = event.get(id)
    except ValueError:
        abort(404)

    return jsonify(dict(
        id=e.id,
        title=e.title,
        location=e.location,
        datetime=e.datetime,
        description=e.description,
        followers=[follower.id for follower in e.followers],
        organisation=e.organisation.id
    ))


def get_event_section(events, page=1, page_length=20):
    """
    Gets a list of events
    :param page: int
    :param page_length: int
    :return: list<Event>
    """
    start_index = (page - 1) * page_length
    end_index = page * page_length - 1

    if start_index < len(events):
        if end_index < len(events):
            return events[start_index:end_index+1]
        else:
            return events[start_index:]
    else:
        raise ValueError('There are no more events')


@e.route('.json')
def api_eventlist():
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 1

    try:
        page_len = int(request.args.get('length'))
    except TypeError:
        page_len = 20

    
    full_events = event.list_events()

    events = []
    try:
        events = get_event_section(
            full_events,
            page=page,
            page_length=page_len
        )
    except ValueError:
        pass

    return jsonify(dict(
        event_count=len(events),
        events=events,
        page=page,
        total_pages=math.ceil(len(full_events) / page_len)
    ))
