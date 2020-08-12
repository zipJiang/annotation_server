from flask import render_template, redirect, request, url_for, flash
from . import annt
from .. import db
from ..models import Progress, AnnotationResult
from flask_login import current_user
import random
import json


@annt.route('/task/<progress_id>', methods=['GET', 'POST'])
def task(progress_id: int):
    """This function run task of a specific id from the progress.
    (task id here is the synonym of progress id.)
    """
    progress = Progress.query.filter_by(id=progress_id).first_or_404()

    # and we render according to progress
    template_name = progress.file.template

    # do the loading.
    if request.method == 'POST':
        # this is a filled form.
        filled_form = request.form

        json_dict = {}
        for key, value in filled_form.items():
            # will rewrite duplicated keys
            json_dict[key] = value

        # and now write info back
        annotation_result = AnnotationResult(result=json.dumps(json_dict),
                                             row_id=progress.current_row_id)
        progress.results.append(annotation_result)
        db.session.commit()

    # comparing finished items and all items
    finished = [item.row_id for item in progress.results.all()]
    all_ = [item.row_id for item in progress.file.annotation_contents.all()]

    remaining = set(all_).difference(set(finished))
    if remaining:
        selected_row_id = random.choice(list(remaining))
        selected_instance = progress.file.annotation_contents.filter_by(row_id=selected_row_id).first_or_404()

        progress.current_row_id = selected_row_id
        db.session.commit()

        # now render the template with this selected instance.
        json_content = json.loads(selected_instance.content)
        return render_template('annt/{}'.format(template_name), content=json_content)
    else:
        return render_template('annt/finished_all.html', user=current_user)
