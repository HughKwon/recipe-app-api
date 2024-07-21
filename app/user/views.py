"""
View for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

# generics.CreateAPIView handles HTTP POST requests designed to create objects (in the database)
# All we have to do is define the serializer, set the serializer class in the view.
# then Django know what model we want to use, because the serializer knows
#   which user model to use (defined in the serializer.py get_user_model, which is defined in the models.py)

# When you make an HTTP request,
# it goes through to the URL (defined in the urls.py) --passes-to--> create user view class
# --> calls the serializer, creates the object, and returns the response
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer

# We're using ObtainAuthToken view (provided by Django), and we're customizing
#  the serializer to create our custom serializer
# because we use email instead of the username (default behavior)
# We're overriding the behavior
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    # optional, but we're using the default renderer classes for the obtainauthtoken view
    # with this, we get the browsable API for Django, allows nice user interface
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# generics.RetrieveUpdateAPIView provides functionality for retrieving and updating objects in the database
# supports HTTP GET, PATCH, and PUT
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer

    # authentication in Django is split into 2 different things:
    # authentication --> how do you know that the user is the user they say they are.
    #                    we use token authentication
    # permission --> we know who the user is, what can the user do in the system?
    #                we want to make sure that the user that uses this API is authenticated
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # we override the get_object, which gets the object for the HTTP GET (or any other) request
    # In this case, we're just retrieving the user that's attached to the request
    # When a user object is authenticated, the user object being authenticated gets assigned to the
    # request object in the view
    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
