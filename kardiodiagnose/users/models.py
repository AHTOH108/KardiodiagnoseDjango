import datetime

from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class Organization(models.Model):
    """
    """
    title = models.CharField(_('organization title'),
                             max_length=1000, null=False)

    token = models.CharField(_('token'), max_length=256,
                             default="", unique=True, null=True, blank=True)

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="organizations")

    created_by = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                      null=True, related_name="organization", verbose_name=_('created_by'))

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return self.title + ', id=' + str(self.pk)

    class Meta:
        db_table = 'organization'


class UserMixin:
    @property
    def is_annotator(self):
        return False

    def has_permission(self, user):
        if user.active_organization in self.organizations.all():
            return True
        return False


class UserLastActivityMixin(models.Model):
    last_activity = models.DateTimeField(
        _('last activity'), default=timezone.now, editable=False)

    def update_last_activity(self):
        print("update_last_activity")
        self.last_activity = timezone.now()
        self.save(update_fields=["last_activity"])

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        print("_create_user")
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('Must specify an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        print("create_user")
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        print("create_superuser")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(UserMixin, AbstractBaseUser, PermissionsMixin, UserLastActivityMixin):
    username = models.CharField(_('username'), max_length=256)
    email = models.EmailField(_('email address'), unique=True, blank=True)

    first_name = models.CharField(_('first name'), max_length=256, blank=True)
    last_name = models.CharField(_('last name'), max_length=256, blank=True)
    phone = models.CharField(_('phone'), max_length=256, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether to treat this user as active. '
                                                'Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    activity_at = models.DateTimeField(
        _('last annotation activity'), auto_now=True)

    active_organization = models.ForeignKey(
        'Organization',
        null=True,
        on_delete=models.SET_NULL,
        related_name='active_users'
    )

    # allow_newsletters = models.BooleanField(
    #     _('allow newsletters'),
    #     null=True,
    #     default=None,
    #     help_text=_('Allow sending newsletters to user')
    # )
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    class Meta:
        db_table = 'htx_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['first_name']),
            models.Index(fields=['last_name']),
            models.Index(fields=['date_joined']),
        ]
