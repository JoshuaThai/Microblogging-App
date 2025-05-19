import datetime

from django.test import TestCase, Client

from ..models import User


class TestSignUp(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create(
            first_name = 'John',
            last_name = 'Doe',
            username='testuser',
            email='email@gmail.com',
            password='pass',
            birthDate= datetime.date(1970, 1, 1),
            role = 'user'
        )
    def test_User_exists(self):
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup(self):
        client = Client()
        response = client.post('/signup/', {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'email@gmail.com',
            'password': 'pass',
            'birthDate': '1970-01-01'
        }, follow=True)
        # check if the form input processed.
        self.assertEqual(response.context['username'], 'testuser')
        self.assertEqual(response.context['email'], 'email@gmail.com')
        self.assertEqual(response.context['password'], 'pass')
        self.assertEqual(response.context['birthDate'], '1970-01-01')
