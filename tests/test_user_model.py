"""Testing of the usermodel and its
functionality with password hashing.
"""
import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):
    """Test the user password functionality.
    """
    def test_password_setter(self):
        user = User(password='cat')
        self.assertTrue(user.password_hash is not None)

    def test_no_password_getter(self):
        user = User(password='cat')
        with self.assertRaise(AttributeError):
            user.password

    def test_password_verification(self):
        user = User(password='cat')
        self.assertTrue(user.verify_password('cat'))
        self.assertFalse(user.verify_password('dog'))

    def test_password_salts_are_random(self):
        user = User(password='cat')
        user_2 = User(password='cat')

        self.assertTrue(user.password_hash != user_2.password_hash)
