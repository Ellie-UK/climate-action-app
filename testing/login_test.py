from flask_testing import TestCase

import users.views
from models import db
from app import app
from users.views import account
from models import User
import unittest
import pyotp

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

class TestUserLogin(BaseTestCase):

    def test_login_page_loads(self):
        tester=app.test_client(self)
        response = self.client.get('/login')
        self.assertTrue(b'Email' in response.data)

    def test_correct_login(self):
        pin = pyotp.TOTP('BFB5S34STBLZCOB22K6PPYDCMZMH46OJ')
        tester=app.test_client(self)
        with self.client:
            responses = tester.get('/account')
            response = tester.post(
                '/login',
                data=dict(email="admin@email.com", password="Admin1!", pin_key=pin.now),
                follow_redirects=True
            )
            self.assertIn(b'You should be redirected automatically to target URL', responses.data)

    def test_incorrect_login(self):
        tester=app.test_client(self)
        with self.client:
            response = tester.post(
                '/login',
                data=dict(email="Wrong", password="wrong", pin_key="123123"),
                follow_redirects=True
            )
            self.assertIn(b'Invalid email address.', response.data)

    def test_incorrect_email(self):
        tester=app.test_client(self)
        with self.client:
            response = tester.post(
                '/login',
                data=dict(email="wrong"),
                follow_redirects=True
            )
            self.assertIn(b'Invalid email address.', response.data)

    def test_incorrect_password(self):
        tester=app.test_client(self)
        with self.client:
            response = tester.post(
                '/login',
                data=dict(password="wrong"),
                follow_redirects=True
            )
            self.assertIn(b'This field is required', response.data)

    def test_incorrect_email_pin(self):
        tester=app.test_client(self)
        with self.client:
            response = tester.post(
                '/login',
                data=dict(pin_key="123123"),
                follow_redirects=True
            )
            self.assertIn(b'This field is required.', response.data)

