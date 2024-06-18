from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BasedUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        Simplified from the original implementation in django.contrib.auth.models.UserManager.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Adapted from UserManager.create_user, but without the username arg.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Adapted from UserManager.create_superuser, but without the username arg.
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class BasedUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract user class that unfortunately re-implements much of `django.contrib.auth.models.AbstractUser`
    but without some unnecessary fields:
    - username
    - first_name
    - last_name
    - date_joined
    """

    email = models.EmailField(_("email address"), unique=True, blank=False)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = BasedUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        self.email = self.__class__.objects.normalize_email(self.email)
