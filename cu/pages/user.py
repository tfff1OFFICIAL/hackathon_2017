"""
Users information
"""
from flask import Blueprint, redirect, render_template, jsonify, abort
from flask_login import current_user, login_required
from cu import googlelogin, user


u = Blueprint(
    "user",
    __name__,
    template_folder='../template'
)


@u.route('/')
def index():
    """
    The index of u
    :return: redirect to u/<user.id> or display register/login
    """
    if current_user.is_authenticated:  # if someone's logged in atm
        return redirect("/u/{}".format(current_user.id))

    return render_template('user/login.shtml', login_link=googlelogin.authorization_url())


@u.route('/<int:id>')
def display_user(id):
    """
    Display the user with id
    :param id: int
    """
    try:
        return render_template('user/view.shtml', user=user.get(id))
    except ValueError:
        abort(404)


@u.route('/logout')
def logout():
    return redirect('/logout')


@u.route('/<int:id>.json', methods=['POST', 'GET'])
@login_required
def api_userdata(id):
    """
    Return the users data
    :param id: int, id of the user
    """
    try:
        id = int(id)
    except ValueError:
        abort(400)

    if current_user.id == id:  # this user can only access it's own data
        return jsonify(dict(
            google_id=current_user.google_id,
            id=current_user.id,
            name=current_user.name,
            active=current_user.active,
            manager=True if current_user.organisation else False,
            organisation=current_user.organisation.id if current_user.organisation else None,
            subscribed_events=[e.id for e in current_user.events_following],
            subscribed_organisations=[o.id for o in current_user.organisations_following]
        ))

    abort(403)
