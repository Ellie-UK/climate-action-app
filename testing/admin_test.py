from app import app
from flask_testing import TestCase
from models import db, User
import pyotp


# get generated user pin for testing purposes
def get_pin():
    user = User.query.get(1)
    pinkey = pyotp.TOTP(user.pin_key)
    return pinkey.now()


class BaseTestCase(TestCase):
    ''' Base test'''

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User(email='admin@email.com',
                            password='password',
                            pin_key='BFB5S34STBLZCOB22K6PPYDCMZMH46OJ',
                            firstname='Jon',
                            lastname='Jones',
                            phone='0191-123-4567',
                            role='admin'))
        db.session.add(User(email='user@email.com',
                            password='password',
                            pin_key='BFB5S34STBLZCOB22K6PPYDCMZMH46OJ',
                            firstname='Will',
                            lastname='Smith',
                            phone='0191-123-4567',
                            role='user'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestAdmin(BaseTestCase):

    # test admin page works for admins
    def test_admin_access_admin(self):
        # user pin
        pin = get_pin()

        with self.client:
            # login
            self.client.post('/login', data=dict(email='admin@email.com', password='password', pin=pin))
            # open admin page
            response = self.client.get('/admin', follow_redirects=True)
            self.assertIn(b'Admin', response.data)

    # test admin page denies access to normal users
    def test_user_access_admin(self):
        # user pin
        pin = get_pin()

        with self.client:
            # login
            self.client.post('/login', data=dict(email='user@email.com', password='password', pin=pin))
            # open admin page
            response = self.client.get('/admin', follow_redirects=False)
            self.assertIn(b'403', response.data)

    # test viewing all users
    def test_view_users(self):
        # user pin
        pin = get_pin()

        with self.client:
            # login
            self.client.post('/login', data=dict(email='admin@email.com', password='password', pin=pin))
            # open admin page
            self.client.get('/admin', follow_redirects=True)
            # click 'view all users' button
            response = self.client.post('/view_users', follow_redirects=True)
            self.assertIn(b'ID', response.data)
