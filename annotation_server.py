"""The main script.
"""
import os
from app import create_app, db
from app.models import User, Role, Progress,\
    AnnotationContent, AnnotationResult, File
from flask_migrate import Migrate


app = create_app('default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """
    """
    return dict(db=db, User=User, Role=Role,
                Progress=Progress, File=File,
                AnnotationContent=AnnotationContent,
                AnnotationResult=AnnotationResult)
