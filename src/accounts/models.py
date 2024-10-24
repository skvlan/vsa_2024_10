from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, User
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.managers import CustomerManager


class Customer(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("name"), max_length=150, blank=True)
    last_name = models.CharField(_("surname"), max_length=120, blank=True)
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    birth_date = models.DateField(_("birth date"), blank=True, null=True)
    photo = models.ImageField("photo", upload_to="img/profiles", blank=True, null=True)
    objects = CustomerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("customer")
        verbose_name_plural = _("customers")

    def __str__(self):
        return str(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_registration_age(self):
        return f"Time on site: {timezone.now() - self.date_joined}"


class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    edit_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Person(BaseModel):
    first_name = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        validators=[MinLengthValidator(2)],
    )
    last_name = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    birth_date = models.DateField(null=True)

    class Meta:
        abstract = True
