from unittest import TestCase
from app import app
from models import db,Post,User

class test(TestCase):

    def setUp(self):
        global users
        global posts
        users = User.query.all()

    def tearDown(self):
        db.session.rollback()

    def test_users_display(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)
            for user in users:
                self.assertIn(user.first_name,html)

    def test_user_details(self):
        with app.test_client() as client:
            res = client.get(f'/users/{users[0].id}')
            html = res.get_data(as_text=True)
            self.assertIn(users[0].first_name,html)

    def test_add_User(self):
        with app.test_client() as client:
            client.post('/users/new',data={'firstNameInput':'John','lastNameInput':'jolaki'})
            new_users = User.query.filter_by(last_name ='jolaki')
            self.assertIsNotNone(new_users)

    def test_add_post(self):
        with app.test_client() as client:
            client.post(f'/users/{users[0].id}/posts/new', data={'titleInput':'testingdb','contentInput':'testing posting a post'})
            new_post = Post.query.filter_by(title='testingdb')
            self.assertIsNotNone(new_post)