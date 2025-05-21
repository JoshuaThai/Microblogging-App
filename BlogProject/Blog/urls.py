from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import HomeView, LoginView, SignUpView, ProfileView, SettingsView

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('signup/', SignUpView.as_view(), name = 'signUp'),
    path('profile/id/<int:id>/', ProfileView.as_view(), name = 'profile'),
    path('settings/id/<int:id>/', SettingsView.as_view(), name = 'settings'),
]