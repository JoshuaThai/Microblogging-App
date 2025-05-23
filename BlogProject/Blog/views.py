from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from .models import User


# Create your views here.
class HomeView(View):
    def get(self, request):
        username = request.session.get('username')
        id = request.session.get('id')
        print(username)
        print('id', id)
        return render(request, 'home.html', {'username': username, 'id': id})
    def post(self, request):
        # need to implement to handle log out button
        request.session.flush() # clear out sessions essentially logging out user.
        return render(request, 'home.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        determineValue = request.POST.get('identifier')
        password = request.POST.get('password')
        if not determineValue or not password:
            return render(request, 'login.html',
                          {'message': 'One or more fields was empty. Please try again.'})
        if User.objects.filter(email=determineValue).first():
            email = determineValue
            user1 = User.objects.filter(email=email).first()
            user = authenticate(request, username=user1.username, password=password)
            if not user:
                return render(request, 'login.html',
                              {'message': 'Invalid password. Please try again.'})
            login(request, user)

            request.session['username'] = user1.username
            request.session['first_name'] = user1.first_name
            request.session['last_name'] = user1.last_name
            request.session['id'] = user1.id
            request.session.save()
        else:
            user1 = User.objects.filter(username=determineValue).first()
            if not user1:
                return render(request, 'login.html',
                              {'message': 'Invalid username or email. Please try again.'})
            user = authenticate(request, username=determineValue, password=password)
            if not user:
                return render(request, 'login.html',
                              {'message': 'Invalid password. Please try again.'})
            login(request, user)
            request.session['username'] = user1.username
            request.session['first_name'] = user1.first_name
            request.session['last_name'] = user1.last_name
            request.session['id'] = user1.id
            request.session.save()

        return redirect('home')

class SignUpView(View):
    def get(self, request):
        return render(request, 'signup.html')
    def post(self, request):
        first_name = request.POST['first_name']
        # handle user not entering their first name
        if not first_name:
            return render(request, 'signup.html', {'message': 'Please enter your first name.'})
        last_name = request.POST['last_name']
        # handle user not entering their first name
        if not last_name:
            return render(request, 'signup.html', {'message': 'Please enter your last name.'})
        email = request.POST['email']
        # check email
        if not email:
            return render(request, 'signup.html', {'message': 'Please enter your email.'})
        if not '@' in email:
            return render(request, 'signup.html', {'message': 'Please enter an valid email address.'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'message': 'This email is already associated with another account. '
                            'Please choose a different email address.'})

        username = request.POST['username']
        # check username
        if not username:
            return render(request, 'signup.html', {'message': 'Please enter an username.'})
        if len(username) < 5:
            return render(request, 'signup.html',
                          {'message': 'Please enter an username that is at least five characters.'})

        password = request.POST['password']
        print('password', password)
        if not password:
            return render(request, 'signup.html', {'message': 'Please enter a password.'})
        if len(password) < 8:
            return render(request, 'signup.html', {'message': 'Password too short! Please enter a password that is at least 8 characters.'})
        if len(password) > 24:
            return render(request, 'signup.html', {'message': 'Password too long! Please enter a password that is at most 24 characters.'})

        birthDate = request.POST['birthDate']
        if not birthDate:
            return render(request, 'signup.html', {'message': 'Please enter your date of birth.'})

        # If passing all the above checks, create the user account.
        user = User(first_name=first_name,
                                   last_name=last_name,
                                   email=email,
                                   username=username,
                                   birthDate=birthDate)
        user.set_password(password)
        user.save()

        # login user
        login(request, user)

        # declare sessions
        request.session['username'] = user.username
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        request.session['id'] = user.id
        request.session.save()

        return redirect('home')

class ProfileView(LoginRequiredMixin, View):
    # @login_required
    def get(self, request, id):
        print('id', id)
        user = User.objects.filter(id=id).first()
        return render(request, 'profile.html', {'profile_user': user})
    def post(self, request, id):
        biography = request.POST.get('bio')
        user = User.objects.filter(id=id).first()
        user.bio = biography
        user.save()
        user = User.objects.filter(id=id).first()
        return render(request, 'profile.html', {'profile_user': user})
class SettingsView(LoginRequiredMixin, View):
    def get(self, request, id):
        print('id', id)
        user = User.objects.filter(id=id).first()
        return render(request, 'settings.html', {'profile_user': user})
    def post(self, request, id):
        action = request.POST.get('action')
        print('action', action)
        if action == 'changeFirst':
            first_name = request.POST.get('first_name')
            user = User.objects.filter(id=id).first()
            if not first_name:
                return render(request, 'settings.html',
                              {'profile_user': user,
                               'message': 'First name cannot be empty. Enter your new first name.'})
            user.first_name = first_name
            user.save()
            user = User.objects.filter(id=id).first()
            return render(request, 'settings.html', {
                'profile_user': user,
                'message': 'Successfully changed your first name.'
            })

        elif action == 'changeLast':
            last_name = request.POST.get('last_name')
            user = User.objects.filter(id=id).first()
            if not last_name:
                return render(request, 'settings.html',
                              {'profile_user': user,
                               'message': 'Last name cannot be empty. Enter your new last name.'})
            user.last_name = last_name
            user.save()
            user = User.objects.filter(id=id).first()
            return render(request, 'settings.html', {
                'profile_user': user,
                'message': 'Successfully changed your last name.'
            })

        elif action == 'changeEmail':
            email = request.POST.get('email')
            user = User.objects.filter(id=id).first()
            if not email:
                return render(request, 'settings.html',
                              {'profile_user': user,
                               'message': 'Email cannot be empty. Enter a valid email.'})
            if '@' not in email:
                return render(request, 'settings.html',{
                    'profile_user': user,
                    'message': 'Invalid email address. Enter a valid email address.'
                })
            find_email = User.objects.filter(email=email).exclude(id=user.id).first()
            if find_email: # check if email is unique
                return render(request, 'settings.html',
                              {'profile_user': user,
                               'message':'This email is already associated with another account. '
                                         'Please enter a different email address.'})
            user.email = email
            user.save()

            user = User.objects.filter(id=id).first()
            return render(request, 'settings.html', {
                'profile_user': user,
                'message': 'Email successfully changed.'
            })
        elif action == 'changeUsername':
            username = request.POST.get('username')
            user = User.objects.filter(id=id).first()
            if not username: # prevent users from entering an empty username
                return render(request, 'settings.html',{
                    'profile_user': user,
                    'message': 'Username cannot be empty. Enter a valid new username.'
                })
            if len(username) < 5:
                return render(request, 'settings.html',{
                    'profile_user': user,
                    'message': 'Username should be at least 5 characters. Enter a valid new username.'
                })
            user.username = username
            user.save()

            user = User.objects.filter(id=id).first()
            return render(request, 'settings.html', {
                'profile_user': user,
                'message': 'Username successfully changed.'
            })
        elif action == 'changeDate':
            birthDate = request.POST.get('birthDate')
            user = User.objects.filter(id=id).first()
            if not birthDate:
                return render(request, 'settings.html',{
                    'profile_user': user,
                    'message': 'Date of birth cannot be empty. Please enter your date of birth.'
                })
            user.birthDate = birthDate
            user.save()

            user = User.objects.filter(id=id).first()
            return render(request, 'settings.html', {
                'profile_user': user,
            'message': 'Date of birth successfully changed.'
            })
        elif action == 'changePass':
            oldPassword = request.POST.get('oldPass')
            newPassword = request.POST.get('newPass')
            user = User.objects.filter(id=id).first()
            if not oldPassword:
                return render(request, 'settings.html',{
                    'profile_user': user,
                    'message': 'Old password cannot be empty. Please enter your old password.'
                })
            # check if the old password matches our records.
            if not user.check_password(oldPassword):
                return render(request, 'settings.html',{
                    'profile_user': user,
                    'message': 'The old password entered does not match our records. '
                               'Please re-enter your old password.'
                })

            if not newPassword:
                return render(request, 'settings.html', {
                    'profile_user': user,
                    'message': 'New password cannot be blank. Please enter a valid new password.'
                })
            if len(newPassword) > 24:
                return render(request, 'settings.html',{
                    'profile_user': user,
                    'message': 'Password too long! Please enter a new password that is at most 24 characters.'
                })
            if len(newPassword) < 8:
                return render(request, 'settings.html',{
                    'profile_user': user,
                    'message': 'Password too short! Please enter a new password that is at least 8 characters.'
                })

            # If valid, update the password
            user.set_password(newPassword)
            user.save()
            user = User.objects.filter(id=id).first()
            return render(request, 'settings.html', {
                'profile_user': user,
                'message': 'Password successfully changed.'
            })
