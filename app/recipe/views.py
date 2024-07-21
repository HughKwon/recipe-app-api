"""
Views for the recipe APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


# ModelViewSet is specifically set up to work directly with Model
# we're going to use a lot of existing logic defined in serializers.py
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeSerializer
    # queryset represents the objects that are available for this viewset
    # Because ModelViewSet is expected to work with a model,
    # we can specify the query set of objects that is going to be manageable
    # through this API or through our model view
    queryset = Recipe.objects.all()
    # in order to access any data it has to use token authentication and be authenticated
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        # adding additional filter to filter by user
        return self.queryset.filter(user=self.request.user).order_by('-id')

