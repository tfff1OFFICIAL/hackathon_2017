from flask import Blueprint, session, request, abort, redirect, url_for, render_template

org = Blueprint(
    '/org',
    __name__,
    template_folder='templates'
)
