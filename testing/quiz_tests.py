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

    # add mock question and user to database
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


# Test that the quiz page runs correctly
class TestQuiz(BaseTestCase):
    @mock.patch('flask_login.utils._get_user')
    def test_quiz(self, current_user):
        # create a mock current_user
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            response = self.client.get('/quiz', follow_redirects=True)
            # check the question is found on the page
            self.assertIn(b'Will this pass?', response.data)

    # Test the submit works for the user
    @mock.patch('flask_login.utils._get_user')
    def test_submit(self, current_user):
        # create a mock current_user
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            self.client.post('/submit', data=dict(question_id=1, answer=1), follow_redirects=True)
            # search for submitted result
            result = Results.query.filter_by(user_id=1).first()
            # check the correct result is found
            self.assertTrue(result.__getattribute__('question_id') == 1)

    # Test create a question
    @mock.patch('flask_login.utils._get_user')
    def test_create_question(self, current_user):
        # create a mock current_user
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            # create new question
            self.client.post('/create_question', data=dict(question='Test?',
                                                           option1='A',
                                                           option2='B',
                                                           option3='C',
                                                           option4='D',
                                                           answer=1))
            # search for new question
            question = Quiz.query.filter_by(question_id=2).first()
            # check question exists
            self.assertIsNotNone(question)

    # Test a question can be updated
    @mock.patch('flask_login.utils._get_user')
    def test_update_question(self, current_user):
        # create a mock current_user
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            # update question
            self.client.post('/1/update_question', data=dict(question='Update?',
                                                             option1='A',
                                                             option2='B',
                                                             option3='C',
                                                             option4='D',
                                                             answer=1))
            # get updated question
            question = Quiz.query.filter_by(question_id=1).first()
            # check question has been updated
            self.assertTrue(question.__getattribute__ ('question') == 'Update?')

    # Test quiz can be reset
    @mock.patch('flask_login.utils._get_user')
    def test_delete_quiz(self, current_user):
        # create a mock current_user
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            # run delete quiz method
            delete_quiz()
            quiz = Quiz.query.all()
            # check quiz table is empty
            self.assertListEqual([], quiz)
            result = Results.query.all()
            # check result table is empty
            self.assertListEqual([], result)

    # Test a user can finish a quiz and score is submitted
    @mock.patch('flask_login.utils._get_user')
    def test_finish_quiz(self, current_user):
        # create mock current_user
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            self.client.post('/submit', data=dict(question_id=1, answer=1), follow_redirects=True)
            self.client.post('/finish_quiz')
            user = User.query.filter_by(id=1).first()
            # check user score has been updated
            self.assertTrue(user.__getattribute__('total_score') == 1)

    # Test leaderboard loads correctly
    @mock.patch('flask_login.utils._get_user')
    def test_leaderboard(self, current_user):
        # create a mock current_user
        user = User.query.get(1)
        current_user.return_value = user
        with self.client:
            response = self.client.get('/leaderboard', follow_redirects=True)
            # check leaderboard page loads
            self.assertIn(b'Leaderboard', response.data)