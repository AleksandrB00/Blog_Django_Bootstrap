from django.urls import path 
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings


urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('signin', SignInView.as_view(), name='signin'),
    path('logout', LogoutView.as_view(), {'next_page' : settings.LOGOUT_REDIRECT_URL}, name='logout'),
]