import pyotp
from app import app
from flask_testing import TestCase
from models import db, User, FAQ


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
        db.session.add(FAQ(question='Can you answer?'))
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


class TestFAQ(BaseTestCase):

    # test opening faq page
    def test_load_faq_page(self):
        # user pin
        pin = get_pin()

        with self.client:
            # login
            self.client.post('/login', data=dict(email='user@email.com', password='password', pin=pin))
            # open faq page
            response = self.client.get('/faq', follow_redirects=True)
            self.assertIn(b'Frequently', response.data)

    # test user can ask questions
    def test_ask_question(self):
        # user pin
        pin = get_pin()

        with self.client:
            # login
            self.client.post('/login', data=dict(email='user@email.com', password='password', pin=pin))
            # open faq page
            self.client.get('/faq', follow_redirects=True)
            # ask question
            response = self.client.post('/question', data=dict(question='Does this work?'), follow_redirects=True)
            self.assertIn(b'Does', response.data)

    # test admin can answer questions
    def test_answer_question(self):
        # user pin
        pin = get_pin()

        with self.client:
            # login
            self.client.post('/login', data=dict(email='admin@email.com', password='password', pin=pin))
            # open faq page
            self.client.get('/faq', follow_redirects=True)
            # answer question
            response = self.client.post('/1/answer', data=dict(question='Formulated question', answer='Here is answer'),
                                        follow_redirects=True)
            self.assertIn(b'answer', response.data)
