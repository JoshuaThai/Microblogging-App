import datetime

from django.test import TestCase, Client
from django.urls import reverse

from ..models import User

class AddBioTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(first_name='John',
            last_name='Doe',
            username='testuser',
            email='email@gmail.com',
            birthDate=datetime.date(1970, 1, 1),
            role='user',
            password='password')
        self.user.set_password('password')
        self.user.save()
        login_successful = self.client.login(username='testuser', password='password')
        print("Login success?", login_successful)

    def test_add_bio(self):
        response = self.client.post(reverse('settings', args=[self.user.id]),{
            'user_id': self.user.id,
            'bio': 'Hi there!'
        })

        # page shouldn't be redirected.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hi there!')