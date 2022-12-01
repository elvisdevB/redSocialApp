from unicodedata import name
from django.urls import path
from app.social.views import feed, profile, register, post
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView

from .views import follow, unfollow


urlpatterns = [
    path('', feed, name="feed"),
    path('profile/', profile, name="profile"),
    path('profile/<str:username>/', profile, name="profile"),
    path('register/', register, name="registrar" ),
    path('login/', LoginView.as_view(template_name="social/login.html"), name="login"),
    path('logout/', LogoutView.as_view(template_name="social/logout.html"), name="logout"),
    path('post/', post, name="postear" ),
    path('follow/<str:username>', follow, name="follow"),
    path('unfollow/<str:username>', unfollow, name="unfollow"),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)