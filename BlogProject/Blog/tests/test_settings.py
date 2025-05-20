import datetime

from django.test import TestCase, Client

from ..models import User

'''
# We will be testing settings page here!
# You should be able to modify everything that user model has
# The only thing you cannot MODIFY:
    # account creation date
    # ID
    # role
# Two cases being tests:
    # Saving new settings unsuccessful
    # Saving new settings successful
'''

class SettingsUnsuccessfulTest(TestCase):
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


        user1 = User(
            first_name='Jane',
            last_name='Doe',
            username='janeDoe',
            email='email@outlook.com',
            birthDate=datetime.date(1970, 1, 1),
            role='user'
        )
        user1.set_password('password')
        user1.save()

    def test_user_model_exists(self):
        self.assertTrue(User.objects.filter(username='testuser').exists())
    def test_user_log_in(self):
        self.client.login(username='testuser', password='password')
    # first name cannot be changed to empty string
    def test_first_name_empty(self):
        client = Client()
        response = client.post('/settings/', {
            'first_name': ''
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First name cannot be empty. Enter your new first name.')
        findUser = User.objects.filter(username='testuser').first()
        self.assertTrue(findUser.first_name != '') # should not be changed.

    def test_last_name_empty(self):
        client = Client()
        response = client.post('/settings/', {
            'last_name': ''
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Last name cannot be empty. Enter your new last name.')
        findUser = User.objects.filter(username='testuser').first()
        self.assertTrue(findUser.last_name != '')  # should not be changed.
# username checks
    def test_username_empty(self):
        client = Client()
        response = client.post('/settings/', {
            'username': ''
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username cannot be empty. '
                                      'Enter a valid new username.')
        findUser = User.objects.filter(username='testuser').first()
        self.assertTrue(findUser.username != '')  # should not be changed.

    def test_username_short(self):
        client = Client()
        response = client.post('/settings/', {
            'username': 'test'
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username should be atleast 5 characters. Enter a valid new username.')
        findUser = User.objects.filter(username='testuser').first()
        self.assertTrue(findUser.username != 'test')  # should not be changed.

# password checks
    # no password at all
    def test_noPassword(self):
        client = Client()
        response = client.post('/settings/', {
            'password': ''
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password cannot be blank. Enter a valid new password.')
        findUser = User.objects.filter(username='testuser').first()
        self.assertTrue(findUser.password != '')  # should not be changed.


        # too short of a password
    def test_shortPassword(self):
        client = Client()
        response = client.post('/settings/', {
            'password': 'e'
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'Password too short! Please enter a new password that is at least 8 characters.')
        findUser = User.objects.filter(username='testuser').first()
        self.assertTrue(findUser.password != 'e')  # should not be changed.
        # too long of a password
    def test_longPassword(self):
        client = Client()
        response = client.post('/settings/', {
            'password': '1234567890123456789012345',
        })
        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'Password too long! Please enter a new password that is at most 24 characters.')
        findUser = User.objects.filter(username='testuser').first()
        self.assertTrue(findUser.password != '1234567890123456789012345')  # should not be changed.


# email checks
    def test_noEmail(self):
        client = Client()
        response = client.post('/settings/', {
            'email': '',
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email cannot be empty. Enter a valid email.')
        findUser = User.objects.filter(username='testuser').first()
        self.assertTrue(findUser.email != '')  # should not be changed.

    # invalid email address
    def test_invalidEmail(self):
        client = Client()
        response = client.post('/settings/', {
            'email': 'johnnymail.com',
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email address. Enter a valid email address.')
        findUser = User.objects.filter(username='testuser').first()
        self.assertTrue(findUser.email != 'johnnymail.com')  # should not be changed.

    # enter an email address that is already used
    def test_uniqueEmail(self):
        client = Client()
        response = client.post('/settings/', {
            'email': 'email@outlook.com',
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This email is already associated with another account. '
                            'Please enter a different email address.')
        find_user = User.objects.filter(username='testuser').first()
        self.assertTrue(find_user.email != 'email@outlook.com')  # should not be changed.

    # Not entering an date of birth
    def test_noDate(self):
        client = Client()
        response = client.post('/settings/', {
            'birthDate': ''
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter your date of birth.')
        find_user = User.objects.filter(username='testuser').first()
        self.assertTrue(find_user.birthDate != '')  # should not be changed.

class SettingsSuccessfulTest(TestCase):
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

        user1 = User(
            first_name='Jane',
            last_name='Doe',
            username='janeDoe',
            email='email@outlook.com',
            birthDate=datetime.date(1970, 1, 1),
            role='user'
        )
        user1.set_password('password')
        user1.save()

    def test_user_model_exists(self):
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_log_in(self):
        self.client.login(username='testuser', password='password')

    # first name cannot be changed to empty string
    def test_first_name_changed(self):
        client = Client()
        response = client.post('/settings/', {
            'first_name': 'Jack'
        })

        # page should be redirected
        self.assertEqual(response.status_code, 302)
        self.assertNotContains(response, 'First name cannot be empty. Enter your new first name.')
        find_user = User.objects.filter(username='testuser').first()
        self.assertTrue(find_user.first_name == 'Jack')  # should be changed.

    def test_last_name_changed(self):
        client = Client()
        response = client.post('/settings/', {
            'last_name': 'Jackson'
        })

        # page should be redirected
        self.assertEqual(response.status_code, 302)
        self.assertNotContains(response, 'Last name cannot be empty. Enter your new last name.')
        find_user = User.objects.filter(username='testuser').first()
        self.assertTrue(find_user.last_name == 'Jack')  # should be changed.

    # username checks
    def test_username_changed(self):
        client = Client()
        response = client.post('/settings/', {
            'username': 'JoeBiden'
        })

        # page should be redirected
        self.assertEqual(response.status_code, 302)
        self.assertNotContains(response, 'Username cannot be empty. '
                                      'Enter a valid new username.')
        self.assertNotContains(response, 'Username should be atleast 5 characters. Enter a valid new username.')
        find_user = User.objects.filter(username='testuser').first()
        self.assertTrue(find_user.username == 'JoeBiden')# should be changed.

    # password checks
    # no password at all
    def test_Password_changed(self):
        client = Client()
        response = client.post('/settings/', {
            'password': 'greatest23'
        })

        # page should be redirected
        self.assertEqual(response.status_code, 302)
        self.assertNotContains(response, 'Password cannot be blank. Enter a valid new password.')
        self.assertNotContains(response,
                            'Password too short! Please enter a new password that is at least 8 characters.')
        self.assertNotContains(response,
                            'Password too long! Please enter a new password that is at most 24 characters.')
        find_user = User.objects.filter(username='testuser').first()
        self.assertTrue(find_user.password == 'greatest23')  # should be changed.
    # email checks
    def test_Email_changed(self):
        client = Client()
        response = client.post('/settings/', {
            'email': 'jimmy@gmail.com',
        })

        # page should be redirected
        self.assertEqual(response.status_code, 302)
        self.assertNotContains(response, 'Email cannot be empty. Enter a valid email.')
        self.assertNotContains(response, 'Invalid email address. Enter a valid email address.')
        self.assertNotContains(response, 'This email is already associated with another account. '
                                      'Please enter a different email address.')
        find_user = User.objects.filter(username='testuser').first()
        self.assertTrue(find_user.email == 'jimmy@gmail.com') # should be changed.


    # Not entering an date of birth
    def test_BirthDate_changed(self):
        client = Client()
        response = client.post('/settings/', {
            'birthDate': '1972-01-05'
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Please enter your date of birth.')
        find_user = User.objects.filter(username='testuser').first()
        self.assertTrue(find_user.birthDate == '1972-01-05') # should be changed.

