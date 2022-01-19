import unittest
from flask_testing import TestCase

from forum.views import delete, forum, update
from models import db, Forum, Comments, Quiz, Results
from app import app, load_user
from models import User
import mock

from quiz.views import delete_quiz


class BaseTestCase(TestCase):
    ''' Base test'''

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(Quiz(question='Will this pass?',
                            option1='Yes',
                            option2='No',
                            option3='No',
                            option4='No',
                            answer=1))
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


class TestQuiz(BaseTestCase):
    @mock.patch('flask_login.utils._get_user')
    def test_quiz(self, current_user):
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            response = self.client.get('/quiz', follow_redirects=True)
            self.assertIn(b'Will this pass?', response.data)

    @mock.patch('flask_login.utils._get_user')
    def test_submit(self, current_user):
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            self.client.post('/submit', data=dict(question_id=1, answer=1), follow_redirects=True)
            result = Results.query.filter_by(user_id=1).first()
            self.assertTrue(result.__getattribute__('question_id') == 1)

    @mock.patch('flask_login.utils._get_user')
    def test_create_question(self, current_user):
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            self.client.post('/create_question', data=dict(question='Test?',
                                                           option1='A',
                                                           option2='B',
                                                           option3='C',
                                                           option4='D',
                                                           answer=1))
            question = Quiz.query.filter_by(question_id=2).first()
            self.assertIsNotNone(question)

    @mock.patch('flask_login.utils._get_user')
    def test_update_question(self, current_user):
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            self.client.post('/1/update_question', data=dict(question='Update?',
                                                             option1='A',
                                                             option2='B',
                                                             option3='C',
                                                             option4='D',
                                                             answer=1))
            question = Quiz.query.filter_by(question_id=1).first()
            self.assertTrue(question.__getattribute__ ('question') == 'Update?')

    @mock.patch('flask_login.utils._get_user')
    def test_delete_quiz(self, current_user):
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            delete_quiz()
            quiz = Quiz.query.all()
            self.assertListEqual([], quiz)
            result = Results.query.all()
            self.assertListEqual([], result)