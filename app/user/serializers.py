"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers

# ModelSerializer (provided by Django rest framework) allows us to automatically validate and save things to a model that we define in the serializer
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    # Where we tell the Django rest framework the model and the fields,
    #  and any additional fields that we're passing to the serializer
    # serializer needs to know which model we're representing
    class Meta:
        model = get_user_model()
        # only want to include the fields that we want the user to be able to change
        fields = ['email', 'password', 'name']
        # python dictionary that allows us to provide extra metadata to the
        #   different fields to tell the Django framework
        # they cannot read the password, write only
        # min_length --> validation option, if user sends password with less than 5 caharacter,
        # it'll throw an 400 bad request error
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # this method allows us to override the behavior of the Serializer when we create new objects out of the serializer
    # by default, the serializer saves the password as clear text, which we don't want. We want it encrypted.
    # So, we use the get_user_model's create_user method(defined in the core.models.py)
    # We're overriding the create method so that we can call get_user_model().objects.create_user & pass in already validated data from our serializer
    # create method will be called AFTER the validation (defined in above Meta),
    #  only if the validation was successful.
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def valdiate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs