"""
Views for the recipe APIs.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient
)
from recipe import serializers

# we want to extend the schema for the 'list' endpoint
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filter',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter'
            )
        ]
    )
)

# ModelViewSet is specifically set up to work directly with Model
# we're going to use a lot of existing logic defined in serializers.py
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    ## serializer_class = serializers.RecipeSerializer
    ## --> this was updated since most of the methods will use the detail end point
    # queryset represents the objects that are available for this viewset
    # Because ModelViewSet is expected to work with a model,
    # we can specify the query set of objects that is going to be manageable
    # through this API or through our model view
    queryset = Recipe.objects.all()
    # in order to access any data it has to use token authentication and be authenticated
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convera a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        # adding additional filter to filter by user
        # return self.queryset.filter(user=self.request.user).order_by('-id')

        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()


    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            # returns a reference to the class! Not the object itself ex. RecipeSerializer()
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    # this is how we override the behavior for when Django RF saves a model in a viewset
    # read into to the DRF docs
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    # actions decorator allows us to sepcify specific HTTP methods that is
    # supported by this custom action
    # details=True means that the specific id of the recipe is applied for the method (POST)
    # specific url_path specified
    # pk is primary key
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            #save the image to the database
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# base class for recipe attributes (tag/ingredients)
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to recipes.',
            )
        ]
    )
)
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # we want to override the default get_queryset functionality
    # so that we only return the queryset objects for the authenticated
    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
            ).order_by('-name').distinct()

# below comment was before refactoring
# we're using viewset since we just need CRUD functionalities (out of the box)
# mixins adds allow listing functionality for models
# this class requires EXACT spelling of the class variables
class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
