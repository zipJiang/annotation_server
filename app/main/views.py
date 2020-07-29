from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .. import db
from ..models import Role, User


@main.route('/', methods=['GET', 'POST'])
def index():
    """Now this is a minimal index file to host the
    main page of our annotation interface.
    """
    return render_template('index.html')
