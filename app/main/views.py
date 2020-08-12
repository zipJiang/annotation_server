from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
import json
from . import main
from .. import db
from ..models import Role, User


@main.route('/', methods=['GET', 'POST'])
def index():
    """Now this is a minimal index file to host the
    main page of our annotation interface.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.user', user=current_user))
    return render_template('index.html')


@main.route('/user')
@login_required
def user():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    return render_template('user.html', user=user)


@main.app_template_filter('get_num_finished')
def get_num_finished(progress):
    return len(progress.results.all())


@main.app_template_filter('get_percent')
def get_percent(progress):
    return "{:.2f}%".format(get_num_finished(progress) / progress.file.hit_num * 100)
