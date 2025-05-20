import datetime

from django import test
from django.contrib.auth import get_user_model
from ..models import User

User = get_user_model()
# unit test for User Models
class TestModels(test.TestCase):
    def setUp(self):
        user = User(
            first_name = 'John',
            last_name = 'Doe',
            username='testuser',
            email='email@gmail.com',
            birthDate= datetime.date(1970, 1, 1),
            role = 'user'
        )
        user.set_password('pass')
        user.save()
    def test_User_exist(self):
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(User.objects.filter(email='email@gmail.com').exists())
        self.assertTrue(User.objects.filter(first_name='John').exists())
    def test_User_has_role(self):
        self.assertTrue(User.objects.filter(role='user').exists())
        self.assertEqual(User.objects.filter(role='user').count(), 1) # should be only one user
    def test_User_Date(self):
        user = User.objects.filter(username='testuser').get()
        self.assertEqual(user.birthDate, datetime.date(1970, 1, 1))