"""
Event view functions
"""
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
