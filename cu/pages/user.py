"""
Users information
"""
from flask import Blueprint


u = Blueprint(
    "user",
    __name__,
    template_folder='../template'
)
