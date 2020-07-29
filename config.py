"""Configuration file for the flasky server.
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Most of these will use
    class-level configuration.
    """
    # TODO: This should be changed to some safer version
    SECRET_KEY = os.environ.get('SECRET_KEY') or '###zj2265###'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Dev
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or\
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestConfig(Config):
    """Test
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or\
        'sqlite://'


class ProductionConfig(Config):
    """Production
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


# define a global config object to be used.
config = {'development': DevelopmentConfig,
          'testing': TestConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig}
