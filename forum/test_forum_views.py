from datetime import datetime
from unittest import TestCase
from app import app
from models import db, User, Forum


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config.TestConfig')
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()
        new_user = User(email='dan@email.com',
                        firstname='Dan',
                        lastname='Man',
                        phone='0191-123-4567',
                        password='Password',
                        pin_key='BFB5S34STBLZCOB22K6PPYDCMZMH46OJ',
                        role='user')
        new_forum = Forum(user_id=1,
                          title='Test',
                          body='This is a test')
        db.session.add(new_user)
        db.session.add(new_forum)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    def test_forum_shows(self):
        response = self.client.get('/forum', follow_redirects=True)
        self.assertIn(b'This is a test', response.data)





