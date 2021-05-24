from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
    Group,
)

class UserManager(BaseUserManager):
    """Class to manage the creation of user objects"""

    def create_user(self, username, email, password=None):
        """Creates and returns a user object
        Arguments:
        username: the string to use as username
        email: the string to use as email
        password: the string to use as password

        Optionals:
        is_staff: Boolean to indicate a user is staff or not
        is_admin: Boolean to indicate a user is an admin or not
        is_active: Boolean to indicate a user can login or not

        Return:
            A user object
        """
        if not username:
            raise ValueError('Users must have a username')

        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(username=username,email = self.normalize_email(email),)
        user.set_password(password)
        user.is_active=True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """Creates an admin user object
        Arguments:
        username: the string to use as username
        email: the string to use as email
        password: the string to use as password

        Return:
            A user object
        """
        user = self.create_user(username, email, password=password)
        user.is_admin=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Class for creating user implementing the abstract
    base user and the permission class
    """
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        """Returns a string representation of this `User`."""
        return self.username

    def delete(self, using=None, keep_parents=False):
        self.is_active ^= True
        self.save()

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

class Role(Group):
    description = models.TextField(max_length=100, unique=True)

    def __str__(self):
        """Returns a string representation of this `Role`."""
        return self.name
