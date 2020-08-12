"""This module removes a task from the database.
"""
from app import create_app, db
from app.models import File, User, Progress, AnnotationContent
from typing import Text
import argparse


def interactive_removal(context: Text):
    """
    """
    app = create_app(context)
    with app.app_context():
        all_files = db.session.query(File).all()
        print('Below please select the item to remove (with id).')
        print('-' * 30)
        for file_instance in all_files:
            print('{}. {} | {}'.format(file_instance.id, file_instance.filename, file_instance.taskname))
        print('-' * 30)

        file_id = input('selected_id:')
        file_ = db.session.query(File).filter_by(id=file_id).first()

        # first delete all annotationcontent of the file
        for annotation_content in file_.annotation_contents.all():
            db.session.delete(annotation_content)

        # then delete all progress related to the file
        for progress in file_.progresses.all():
            for annotation_result in progress.results:
                db.session.delete(annotation_result)

            db.session.delete(progress)

        # then we remove the file we are using.
        db.session.delete(file_)
        db.session.commit()


if __name__ == '__main__':
    """We remove a database either by filename or by taskname.
    (We do this interactively thus we may have an idea of all post and select)
    """
    PARSER = argparse.ArgumentParser(
        """Specify a context for the removal to act upon.
        """
    )
    PARSER.add_argument('--context', action='store', dest='context',
                        required=False, default='default', type=str,
                        help='App context to specify which database to use.')

    ARGS = PARSER.parse_args()
    interactive_removal(ARGS.context)
