from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from apps.users.views import CreateUserView, UserDetailView

urlpatterns = [
    path('auth/login/', obtain_auth_token),
    path('auth/register/', CreateUserView.as_view(), name='register'),
    path('current/', UserDetailView.as_view(), name='user'),
]
