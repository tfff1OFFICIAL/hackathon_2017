from flask import Blueprint, session, request, abort, redirect, url_for, render_template
from flask_login import current_user, login_required
from cu import organisation

org = Blueprint(
    'organisation',
    __name__,
    template_folder='../template'
)


@org.route("/register", methods=["GET", "POST"])
@login_required
def register():
    """
    Register a new Organisation
    """
    if not current_user.organisation:
        from .form import CreateOrganisationForm

        form = CreateOrganisationForm(request.form)
        if request.method == 'POST' and form.validate():
            # Create the organisation
            return str(organisation.create(form.name.data, current_user, form.description.data))
        return render_template('org/register.shtml', form=form)
    else:
        return redirect("/org/%i" % current_user.organisation.id)


@org.route("/<int:id>")
def view_organisation(id):
    """
    View the organisation
    :param id: int, id of the organisation
    """
    try:
        o = organisation.get(int(id))
    except ValueError:
        abort(404)
    else:
        return render_template('org/view.shtml', org=o)

@org.route('/<int:id>/follow', methods=['POST', 'GET'])
@login_required
def add_follower(id):
    """
    Adds the current user as a follower of organisation id
    :param id: int, the id of the current organisation
    """
    try:
        current_user.follow_organisation(organisation.get(id))
        organisation.commit_changes()
    except ValueError:
        abort(400)

@org.route('/<int:id>/unfollow', methods=['POST', 'GET'])
@login_required
def rem_follower(id):
    """
    Removes the current user as a follower of event id
    :param id: int, the id of the current event
    """
    try:
        current_user.unfollow_event(organisation.get(id))
        organisation.commit_changes()
    except ValueError:
        abort(400)
