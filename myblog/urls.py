from django.urls import path 
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings


urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('signin', SignInView.as_view(), name='signin'),
    path('logout', LogoutView.as_view(), {'next_page' : settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('create_post', CreatePostView.as_view(), name='create_post'),
    path('blog/<slug>', PostPageView.as_view(), name='post_detail'),
    path('profile_page', EditProfileView.as_view(), name='profile_page'),
    path('search', SearchView.as_view(), name='search_results'),
]