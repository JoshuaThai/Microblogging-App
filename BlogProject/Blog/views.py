from django.shortcuts import render
from django.views import View


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

class SignUpView(View):
    def get(self, request):
        return render(request, 'signup.html')
