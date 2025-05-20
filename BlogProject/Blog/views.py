from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View

from .models import User


# Create your views here.
class HomeView(View):
    def get(self, request):
        username = request.session.get('username')
        print(username)
        return render(request, 'home.html', {'username': username})
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
        request.session.save()

        return redirect('home')