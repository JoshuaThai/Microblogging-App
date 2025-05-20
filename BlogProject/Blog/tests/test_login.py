import datetime

from django.test import TestCase, Client

from ..models import User

'''
# For login, we will be checking if it is successful or unsucessful.
# For Login, we should be able to able to enter the username or the email to log in alongside a password.
# For Unsuccessful Tests:
    # We will test if we enter the wrong username
    # We will test if we enter the wrong email
    # We will test if we enter the wrong password
# For successful Tests:
    # We will test if we enter the correct username and password
    # We will test if we enter the correct email and password
'''
class LoginUnsuccessfulTests(TestCase):
    def setUp(self):
        self.client = Client()
        user = User(
            first_name = 'John',
            last_name = 'Doe',
            username='testuser',
            email='email@gmail.com',
            birthDate= datetime.date(1970, 1, 1),
            role = 'user'
        )
        user.set_password('password')
        user.save()
    def test_user_exists(self):
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_wrong_username(self):
        client = Client()
        response = client.post('/login/', {'identifier': 'testuse', 'password': 'password'})

        self.assertTrue(response.status_code == 200) # page should be rendering again if incorrect info.
        self.assertFalse(response.status_code == 302)  # should not be redirecting anywhere
        self.assertContains(response, 'Invalid username or email. Please try again.')
    def test_login_empty_username(self):
        client = Client()
        response = client.post('/login/', {'identifier': '', 'password': 'password'})
        self.assertTrue(response.status_code == 200)  # page should be rendering again if incorrect info.
        self.assertFalse(response.status_code == 302)  # should not be redirecting anywhere
        self.assertContains(response, 'One or more fields was empty. Please try again.')

    def test_login_wrong_email(self):
        client = Client()
        response = client.post('/login/', {'identifier': 'josh@email.com', 'password': 'password'})

        self.assertTrue(response.status_code == 200) # page should be rendering again if incorrect info.
        self.assertFalse(response.status_code == 302) # should not be redirecting anywhere
        self.assertContains(response, 'Invalid username or email. Please try again.')
    def test_login_wrong_password(self):
        client = Client()
        response = client.post('/login/', {'identifier': 'testuser', 'password': 'pass'})

        self.assertTrue(response.status_code == 200) # page should be rendering again if incorrect info.
        self.assertFalse(response.status_code == 302) # should not be redirecting anywhere
        self.assertContains(response, 'Invalid password. Please try again.')

    def test_login_empty_password(self):
        client = Client()
        response = client.post('/login/', {'identifier': '', 'password': ''})

        self.assertTrue(response.status_code == 200)  # page should be rendering again if incorrect info.
        self.assertFalse(response.status_code == 302)  # should not be redirecting anywhere
        self.assertContains(response, 'One or more fields was empty. Please try again.')

class LoginSuccessfulTests(TestCase):
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
    def test_login_correct_username(self):
        client = Client()
        response = client.post('/login/', {'identifier': 'testuser', 'password': 'password'})

        self.assertFalse(response.status_code == 200)
        self.assertTrue(response.status_code == 302) # should redirect now!
    def test_login_correct_email(self):
        client = Client()
        response = client.post('/login/', {'identifier': 'email@gmail.com', 'password': 'password'},
                               follow=True)

        # when checking responses, always use contains assert!
        self.assertNotContains(response, 'One or more fields was empty. Please try again.')
        self.assertContains(response, 'Welcome, testuser!')
        # if I want to do this line, I need follow=true
