import datetime

from django.test import TestCase, Client

from ..models import User

class SignUpUnsuccessfulTests(TestCase):
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
        user.set_password('pass')
        user.save()
    def test_User_exists(self):
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup_noFirst(self):
        client = Client()
        response = client.post('/signup/', {
            'first_name': '',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'email@email.com',
            'password': 'pass',
            'birthDate': '1970-01-01'
        }, follow=True)
        self.assertEqual(response.status_code, 200) # site reloaded the page atleast.
        self.assertContains(response, 'Please enter your first name.')
    def test_signup_noLast(self):
        client = Client()
        response = client.post('/signup/', {
            'first_name': 'John',
            'last_name': '',
            'username': 'testuser',
            'email': 'email@email.com',
            'password': 'pass',
            'birthDate': '1970-01-01'
        }, follow=True)
        self.assertEqual(response.status_code, 200) # site reloaded the page atleast.
        self.assertContains(response, 'Please enter your last name.')
    def test_signup_noEmail(self):
        client = Client()
        response = client.post('/signup/', {
            'first_name': 'john',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': '',
            'password': 'pass',
            'birthDate': '1970-01-01'
        }, follow=True)
        self.assertEqual(response.status_code, 200) # site reloaded the page atleast.
        self.assertContains(response, 'Please enter your email.')
    # invalid email address
    def test_signup_invalidEmail(self):
        client = Client()
        response = client.post('/signup/', {
            'first_name': 'john',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'johnnymail.com',
            'password': 'pass',
            'birthDate': '1970-01-01'
        }, follow=True)
        self.assertEqual(response.status_code, 200) # site reloaded the page atleast.
        self.assertContains(response, 'Please enter an valid email address.')

    # enter an email address that is already used
    def test_signup_uniqueEmail(self):
        client = Client()
        response = client.post('/signup/', {
            'first_name': 'john',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'email@gmail.com',
            'password': 'pass',
            'birthDate': '1970-01-01'
        }, follow=True)
        self.assertEqual(response.status_code, 200) # site reloaded the page atleast.
        self.assertContains(response,
                            'This email is already associated with another account. '
                            'Please choose a different email address.')

    # username tests
    # no username at all.
    def test_signup_noUsername(self):
        client = Client()
        response = client.post('/signup/', {
            'first_name': 'john',
            'last_name': 'Doe',
            'username': '',
            'email': 'email@email.com',
            'password': 'pass',
            'birthDate': '1970-01-01'
        }, follow=True)
        self.assertEqual(response.status_code, 200)  # site reloaded the page atleast.
        self.assertContains(response, 'Please enter an username.')
    # username is too short
    def test_signup_shortUsername(self):
        client = Client()
        response = client.post('/signup/', {
            'first_name': 'john',
            'last_name': 'Doe',
            'username': 's',
            'email': 'email@email.com',
            'password': 'pass',
            'birthDate': '1970-01-01'
        }, follow=True)
        self.assertEqual(response.status_code, 200)  # site reloaded the page atleast.
        self.assertContains(response, 'Please enter an username that is at least five characters.')

    # password tests
    # no password at all
    def test_signup_noPassword(self):
        client = Client()
        response = client.post('/signup/', {
            'first_name': 'john',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'email@email.com',
            'password': '',
            'birthDate': '1970-01-01'
        }, follow=True)
        self.assertEqual(response.status_code, 200)  # site reloaded the page atleast.
        self.assertContains(response, 'Please enter a password.')

    # too short of a password
    def test_signup_shortPassword(self):
        client = Client()
        response = client.post('/signup/', {
            'first_name': 'john',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'email@email.com',
            'password': 'e',
            'birthDate': '1970-01-01'
        }, follow=True)
        self.assertEqual(response.status_code, 200)  # site reloaded the page atleast.
        self.assertContains(response, 'Password too short! Please enter a password that is at least 8 characters.')

    # too long of a password
    def test_signup_longPassword(self):
        client = Client()
        response = client.post('/signup/', {
            'first_name': 'john',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'email@email.com',
            'password': '1234567890123456789012345',
            'birthDate': '1970-01-01'
        }, follow=True)
        self.assertEqual(response.status_code, 200)  # site reloaded the page atleast.
        self.assertContains(response, 'Password too long! Please enter a password that is at most 24 characters.')

    # Not entering an date of birth
    def test_signup_noDate(self):
        client = Client()
        response = client.post('/signup/', {
            'first_name': 'john',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'email@email.com',
            'password': 'password123',
            'birthDate': ''
        }, follow=True)
        self.assertEqual(response.status_code, 200)  # site reloaded the page atleast.
        self.assertContains(response, 'Please enter your date of birth.')

class SignUpSuccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        TestUser = User.objects.create(
            first_name = 'John',
            last_name = 'Doe',
            username='testuser',
            email='email@gmail.com',
            birthDate= datetime.date(1970, 1, 1),
            role = 'user'
        )
        TestUser.set_password('pass')
        TestUser.save()
    def test_User_exists(self):
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup(self):
        client = Client()
        response = client.post('/signup/', {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'testuser1',
            'email': 'email@email.com',
            'password': 'password123',
            'birthDate': '1970-01-01'
        })
        # check if the form input processed.
        # Will not show if follow=true in response above because it will follow the 302 redirect before it
        # gets to this line.
        self.assertEqual(response.status_code, 302)  # redirected the page atleast.

        # if successful when signing up, a user model should have been created.
        # Also 'user' should have been passed through the render request.
        self.assertTrue(response.wsgi_request.user.is_authenticated)


