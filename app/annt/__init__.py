"""Init a blueprint.
"""
from flask import Blueprint

annt = Blueprint('annt', __name__)

from . import views, errors
