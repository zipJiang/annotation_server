"""Scripts for generating a pesudo task.
"""
import json
from app import create_app, db
from app.models import File, User, Progress, AnnotationContent
import argparse


def upload_to_database(config: argparse.Namespace):
    """This function configure a task and makes
    it available to a specified subset of users.
    """
    with open(config.json_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        assert isinstance(data, list), "The outer-most data structure must be List[...]"

    username_total = None
    if config.user_file is not None:
        with open(config.user_file, 'r', encoding='utf-8') as user_file:
            username_total = [line.strip() for line in user_file]

    app = create_app(config.context)
    with app.app_context():

        file_ = File(filename=config.json_file,
                     taskname=config.title, description=config.desc,
                     hit_num=len(data), template=config.template_file)
        for ridx, row in enumerate(data):
            json_str = json.dumps(row)
            annotation_content = AnnotationContent(content=json_str, row_id=ridx)
            db.session.add(annotation_content)
            file_.annotation_contents.append(annotation_content)

        if username_total is None:
            users = db.session.query(User).all()
        else:
            users = db.session.query(User).filter(User.username in username_total)

        for user in users:
            # we create an individual progress for each user.
            progress = Progress()
            file_.progresses.append(progress)
            user.progresses.append(progress)

            db.session.add(progress)

        db.session.add(file_)
        db.session.commit()


if __name__ == '__main__':
    """This module is used to add a new file of *.json batch to the dataset.
    To upload a batch we need to specify the following properties:

    json_file: Text --- Path to the json file of data the outer-most structure must be a list.
    user_file: Text --- Path to the user_list file, could be none in that case we'll log the task to all existing users.
    template_file: Text -- Path to the template_file we use for the anntation (html file).
    """
    PARSER = argparse.ArgumentParser(
        """Argument Parser for data uploading.
        """
    )
    PARSER.add_argument('--json_file', action='store', dest='json_file',
                        required=True, type=str, help='data batch file.')
    PARSER.add_argument('--user_file', action='store', dest='user_file',
                        required=False, default=None, help='user file (each line a single user.)')
    PARSER.add_argument('--template_file', action='store', dest='template_file',
                        required=True, action='store', dest='template_file',
                        help='Template file to be rendered (.html).')
    PARSER.add_argument('--desc', action='store', dest='desc',
                        required=True, type=str, help='Description of the task.')
    PARSER.add_argument('--title', action='store', dest='title',
                        required=True, type=str, dest='title')

    PARSER.add_argument('--context', action='store', dest='context',
                        required=False, default='default', type=str,
                        help='App context to specify which database to use.')

    ARGS = PARSER.parse_args()

    upload_to_database(ARGS)
