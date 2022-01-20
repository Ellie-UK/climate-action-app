import unittest
from flask_testing import TestCase

from forum.views import delete, forum, update
from models import db, Forum, Comments
from app import app, load_user
from models import User
import mock


class BaseTestCase(TestCase):
    ''' Base test'''

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    # add a mock user and foru to database
    def setUp(self):
        db.create_all()
        db.session.add(Forum(user_id=1, title='Test', body='This is a test'))
        db.session.add(User(email='Jerry@email.com',
                            password='Password',
                            pin_key='BFB5S34STBLZCOB22K6PPYDCMZMH46OJ',
                            firstname='Jerry',
                            lastname='Jones',
                            phone='0191-123-4567',
                            role='user'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


# test the forum page opens correctly
class TestForum(BaseTestCase):
    def test_forum(self):
        with self.client:
            self.client.post('/login', data=dict(email='Jerry@email.com', password='Password', pin='000000'))
            response = self.client.get('/forum', follow_redirects=True)
            self.assertIn(b'This is a test', response.data)

    """def test_delete_forum(self):
        with self.client:
            response = self.client.post(/)"""


# Test the user can create a forum
class TestCreateForum(BaseTestCase):
    @mock.patch('flask_login.utils._get_user')
    def test_create_forum(self, current_user):
        # create a mock current_user
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            self.client.post('/login', data=dict(email='Jerry@email.com', password='Password', pin='000000'))
            # access forum page
            self.client.get('/forum', follow_redirects=True)
            # access create
            response = self.client.post('/create', data=dict(title='Create post', body='Forum created'),
                                        follow_redirects=True)
            # check new forum is found on forum page
            self.assertIn(b"Forum created", response.data)


# Test the user can delete a test
class TestDeleteForum(BaseTestCase):
    def test_delete_forum(self):
        with self.client:
            delete(1)
            # query for the post just deleted
            forum = Forum.query.filter_by(post_id=1).first()
            # check the post no longer exists
            self.assertIsNone(forum)


# Test the forum can be updated
class TestUpdateForum(BaseTestCase):
    @mock.patch('flask_login.utils._get_user')
    def test_update_forum(self, current_user):
        # create a mock current_user
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            self.client.post('/1/update', data=dict(title='Updated', body='Test'), follow_redirects=True)
            post = Forum.query.filter_by(post_id=1).first()
            # check for updated post on forum page
            self.assertTrue(post.__getattribute__('title') == 'Updated')


# Test a comment can be created
class TestComments(BaseTestCase):
    @mock.patch('flask_login.utils._get_user')
    def test_comment(self, current_user):
        # create a mock current_user
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            self.client.post('/1/comment', data=dict(body='comment'), follow_redirects=True)
            # search for new comment
            comment = Comments.query.filter_by(post_id=1).first()
            # check the comment exists
            self.assertTrue(comment.__getattribute__('body') == 'comment')

    # Test that a comment can be viewed on the correct forum post
    @mock.patch('flask_login.utils._get_user')
    def test_view_comment(self, current_user):
        # create a mock current_user
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            response = self.client.get('/1/view_comments', follow_redirects=True)
            # check the comment is found
            self.assertIn(b'comment', response.data)

    # check a user can be delete a comment
    @mock.patch('flask_login.utils._get_user')
    def test_delete_comment(self, current_user):
        # create a mock current_user
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            self.client.post('/1/delete_comment', follow_redirects=True)
            comment = Comments.query.filter_by(post_id=1).first()
            # check comment no longer exists
            self.assertIsNone(comment)
