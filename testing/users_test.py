import unittest
from flask_testing import TestCase
from models import db
from app import app
from models import User


class BaseTestCase(TestCase):
    ''' Base test'''

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestUserRegistration(BaseTestCase):

    def test_user_registration(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                email='admin@email.com',
                password='Admin1!',
                confirm_password='Admin1!',
                pin_key='BFB5S34STBLZCOB22K6PPYDCMZMH46OJ',
                firstname='Alice',
                lastname='Jones',
                phone='0191-123-4567',
                role='admin'), follow_redirects=True)
            self.assertIn(b"Account created. You may now log in.", response.data)
            user = User.query.filter_by(email='admin@email.com').first()
            self.assertTrue(user.__getattribute__('email') == 'admin@email.com')

    def test_incorrect_user_registration(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                email='admin',
                password='Admin1!',
                confirm_password='Admin1!',
                pin_key='BFB5S34STBLZCOB22K6PPYDCMZMH46OJ',
                firstname='Alice',
                lastname='Jones',
                phone='0191-123-4567',
                role='admin'), follow_redirects=True)
            self.assertIn(b'Invalid email address.', response.data)
