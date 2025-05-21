import datetime

from django.test import TestCase, Client
from django.urls import reverse

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
        self.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            username='testuser',
            email='email@gmail.com',
            birthDate=datetime.date(1970, 1, 1),
            role='user',
            password='password'
        )


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
        login_successful = self.client.login(username='testuser', password='password')
        print("Login success?", login_successful)

    def test_user_model_exists(self):
        self.assertTrue(User.objects.filter(username='testuser').exists())
    # first name cannot be changed to empty string
    def test_first_name_empty(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changeFirst',
            'first_name': ''
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First name cannot be empty. Enter your new first name.')

        self.assertTrue(self.user.first_name != '') # should not be changed.

    def test_last_name_empty(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changeLast',
            'last_name': ''
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Last name cannot be empty. Enter your new last name.')
        self.assertTrue(self.user.last_name != '')  # should not be changed.
# username checks
    def test_username_empty(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changeUsername',
            'username': ''
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username cannot be empty. '
                                      'Enter a valid new username.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.username != '')  # should not be changed.

    def test_username_short(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changeUsername',
            'username': 'test'
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username should be at least 5 characters. Enter a valid new username.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.username != 'test')  # should not be changed.

# password checks
    # old password not entered
    def test_no_old_Password(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changePass',
            'oldPass': '',
            'newPass': 'password'
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Old password cannot be empty. Please enter your old password.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.password != '')  # should not be changed.

    # old password not entered
    def test_no_new_Password(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changePass',
            'oldPass': 'password',
            'newPass': ''
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New password cannot be blank. Please enter a valid new password.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.password != '')  # should not be changed.


        # too short of a password
    def test_shortPassword(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changePass',
            'oldPass': 'password',
            'newPass': 'pass'
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'Password too short! Please enter a new password that is at least 8 characters.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.password != 'e')  # should not be changed.
        # too long of a password
    def test_longPassword(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changePass',
            'oldPass': 'password',
            'newPass': '1234567890123456789012345',
        })
        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'Password too long! Please enter a new password that is at most 24 characters.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.password != '1234567890123456789012345')  # should not be changed.

    def test_incorrect_old_password(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changePass',
            'oldPass': 'greater52',
            'newPass': 'password123'
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'The old password entered does not match our records. '
                                     'Please re-enter your old password.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.password != 'password123')  # should not be changed.

# email checks
    def test_noEmail(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action':'changeEmail',
            'email': '',
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email cannot be empty. Enter a valid email.')

        self.assertTrue(self.user.email != '')  # should not be changed.

    # invalid email address
    def test_invalidEmail(self):

        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action':'changeEmail',
            'email': 'johnnymail.com',
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email address. Enter a valid email address.')
        self.assertTrue(self.user.email != 'johnnymail.com')  # should not be changed.

    # enter an email address that is already used
    def test_uniqueEmail(self):

        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action':'changeEmail',
            'email': 'email@outlook.com',
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This email is already associated with another account. '
                            'Please enter a different email address.')

        self.assertTrue(self.user.email != 'email@outlook.com')  # should not be changed.

    # Not entering an date of birth
    def test_noDate(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action':'changeDate',
            'birthDate': ''
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Date of birth cannot be empty. Please enter your date of birth.')
        self.assertTrue(self.user.birthDate != '')  # should not be changed.

class SettingsSuccessfulTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            username='testuser',
            email='email@gmail.com',
            birthDate=datetime.date(1970, 1, 1),
            role='user',
            password='password'
        )

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
        login_successful = self.client.login(username='testuser', password='password')
        print("Login success?", login_successful)

    def test_user_model_exists(self):
        self.assertTrue(User.objects.filter(username='testuser').exists())

    # first name cannot be changed to empty string
    def test_first_name_changed(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changeFirst',
            'first_name': 'Jack'
        })

        # page should be redirected
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'First name cannot be empty. Enter your new first name.')
        self.assertContains(response,'Successfully changed your first name.')

        find_user = User.objects.filter(username='testuser').first()
        self.assertTrue(find_user.first_name == 'Jack')  # should be changed.

    def test_last_name_changed(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changeLast',
            'last_name': 'Jackson'
        })

        # page should be redirected
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Last name cannot be empty. Enter your new last name.')

        self.assertTrue(self.user.last_name != 'Jackson')  # should be changed.

    # username checks
    def test_username_changed(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changeUsername',
            'username': 'JoeBiden'
        })

        # page should be redirected
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Username cannot be empty. '
                                      'Enter a valid new username.')
        self.assertNotContains(response, 'Username should be atleast 5 characters. Enter a valid new username.')
        self.assertContains(response, 'Username successfully changed.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.username == 'JoeBiden')# should be changed.

    # password check
    def test_Password_changed(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changePass',
            'oldPass': 'password',
            'newPass': 'greatest23'
        })

        # page should be redirected
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Old password cannot be empty. Please enter your old password.')
        self.assertNotContains(response, 'New password cannot be blank. Please enter a valid new password.')
        self.assertNotContains(response,
                            'Password too short! Please enter a new password that is at least 8 characters.')
        self.assertNotContains(response,
                            'Password too long! Please enter a new password that is at most 24 characters.')
        self.assertNotContains(response,
                               'Old password does not match our records. Please re-enter your old password.')
        self.assertContains(response,'Password successfully changed.')
        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password('greatest23'))  # should be changed.
    # email checks
    def test_Email_changed(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changeEmail',
            'email': 'jimmy@gmail.com',
        })

        # page should be redirected
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Email cannot be empty. Enter a valid email.')
        self.assertNotContains(response, 'Invalid email address. Enter a valid email address.')
        self.assertNotContains(response, 'This email is already associated with another account. '
                                      'Please enter a different email address.')
        self.assertContains(response, 'Email successfully changed.')

        self.user.refresh_from_db() # refresh the database

        self.assertFalse(self.user.email == 'email@gmail.com')
        self.assertTrue(self.user.email == 'jimmy@gmail.com') # should be changed.

    def test_BirthDate_changed(self):
        response = self.client.post(reverse('settings', args=[self.user.id]), {
            'action': 'changeDate',
            'birthDate': '1972-01-05'
        })

        # page should be rendered or reloaded as settings was invalid.
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Please enter your date of birth.')
        self.assertContains(response, 'Date of birth successfully changed.')
        self.user.refresh_from_db()

        self.assertEqual(self.user.birthDate, datetime.date(1972, 1, 5)) # should be changed.

