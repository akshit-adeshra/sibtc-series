from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """ User Model. """
    # fields defined here will be made mandatory by default
    username = None
    first_name = models.CharField(_('first name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.IntegerField(_('phone'), null=True)
    dob = models.DateField(_('date of birth'), null=True)
    tnc = models.BooleanField(_('Terms & Conditions'), max_length=255, default=False, blank=False, null=False)

    USERNAME_FIELD = 'email'

    # the fields you specify in the 'REQUIRED_FIELDS', are asked when you create the superuser from shell.
    REQUIRED_FIELDS = []

    objects = UserManager()

    # full_name here depicts the custom property we made to display it in the admin panel's list_display field
    @property  # this is optional
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)
    # now in admin.py, we can add "full_name" in list_display
