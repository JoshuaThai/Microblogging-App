import datetime

from django.test import TestCase, Client
from django.urls import reverse

from ..models import User, Post


class AddBioTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.post = Post.objects.all()
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
        response = self.client.post(reverse('profile', args=[self.user.id]),{
            'action': 'editBio',
            'bio': 'Hi there!'
        }, follow=True)

        # page shouldn't be redirected.
        # self.assertEqual(response.status_code, 302)
        self.assertContains(response, 'Hi there!')
class CreatePostTests(TestCase):
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
    def test_add_post(self):
        response = self.client.post(reverse('profile', args=[self.user.id]),{
            'action': 'createPost',
            'post' : 'Hello there!'
        }, follow=True)

        # page should be reloaded
        # self.assertEqual(response.status_code, 302)
        self.assertContains(response, 'Hello there!')

    def test_add_empty_post(self):
        response = self.client.post(reverse('profile', args=[self.user.id]),{
            'action': 'createPost',
            'post': ''
        }, follow=True)

        post = Post.objects.filter(author=self.user, text='').first()
        self.assertFalse(post) # check if post was created, it shouldn't have been
        self.assertContains(response, 'Post cannot be empty!')
