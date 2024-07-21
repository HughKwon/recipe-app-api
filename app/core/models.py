"""
Database models.
"""
# brings in cofigurations from settings.py
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    # this method needs to be spelled correctly
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address')
        # self.model --> defining a new user
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # user.set_password automatically hash encrypted
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# AbstractBaseUser contains the fucntionality for the authentication,
# but no fields
# PermissionsMixin contains the functionality for the permissions & fields
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # defines the field that we want to use for authentication.
    # Replaces 'username' field with 'email'
    USERNAME_FIELD = 'email'

class Recipe(models.Model):
    """Recipe object."""
    # Foreign key allows us to set up a relationship between this Recipe model
    # and another model

    # settings.AUTH_USER_MODEL is what we defined in the settings.py
    # although we could just write out 'core.User', but it's BEST PRACTICE, to
    # reference it from settings because if we do change the user model, we can
    # just change it in one place: settings.py
    # on_delete=models.CASCADE --> if the user object is removed, all the recipe are
    # also removed.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    # in certain DBs (ex. MySQL, not PostgreSQL), TextField can be slower than CharField
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    # this allows the object to be listed as the title, not ID
    def __str__(self):
        return self.title