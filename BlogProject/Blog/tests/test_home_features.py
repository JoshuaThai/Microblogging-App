import datetime

from django.test import TestCase, Client

from ..models import User

'''
We will be testing home features here!
'''

class LogOutTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = User(
            first_name='John',
            last_name='Doe',
            username='testuser',
            email='email@gmail.com',
            birthDate=datetime.date(1970, 1, 1),
            role='user'
        )
        user.set_password('password')
        user.save()
    def test_user_exists(self):
        self.assertTrue(User.objects.filter(username='testuser').exists())
    def test_login(self):
        self.client.login(username='testuser', password='password')
    def test_logout(self):
        client = Client()
        response = client.post('', {'action':'logout'})

        self.assertEqual(200, response.status_code) # should render the home page
        self.assertFalse(response.wsgi_request.user.is_authenticated) # should be false since user is logged out
