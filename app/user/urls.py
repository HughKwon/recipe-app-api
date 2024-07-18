"""
URL mappings for the user API.
"""
from django.urls import path

from user import views

# this allows the user.tests.test_user_api.py to find the URL using the 'reverse'
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name ='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]