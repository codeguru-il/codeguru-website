import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


def validate_center(value):
    if len(value) == 3 and value.isalpha() and value.isascii():
        return value
    raise ValidationError("Center should be represented with 3 letters in english.")


def validate_length(number, length=10):
    if len(str(number)) != length:
        raise ValidationError("%s is not the correct length" % number)


INVITE_TIMEOUT = 48


def group_name_validator(name):
    expression = re.compile(R"^[a-zA-Z0-9_]+$")
    if not expression.match(name):
        # translating using "_()" https://docs.djangoproject.com/en/5.1/ref/forms/validation/#raising-validationerror
        raise ValidationError(
            _("Group name is invalid. Groups names may only include alphanumerical characters and underscores")
        )
    return name


class Competition(models.Model):
    """
    A CodeGuru competition.

    Examples: CGX 2024, CGX 2024 Young, CGX 2024.5
    """

    name = models.CharField(max_length=50, unique=True)
    survivor_signature_enabled = models.BooleanField(default=True)
    survivor_signature_gap = models.PositiveIntegerField(default=49)
    survivor_signature_offset = models.PositiveIntegerField(default=0)
    survivor_signature_value = models.PositiveIntegerField(
        validators=[MinValueValidator(0x00), MaxValueValidator(0xFF)], default=0x90
    )
    survivor_max_length = models.PositiveIntegerField(default=512)

    def __str__(self):
        return self.name


class Center(models.Model):
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=3, unique=True, validators=[validate_center])

    def __str__(self) -> str:
        return f"{self.ticker} - {self.name}"

    def save(self, *args, **kwargs):
        self.ticker = self.ticker.upper()
        return super(Center, self).save(*args, **kwargs)


class CgGroup(models.Model):
    name = models.CharField(max_length=30, unique=True, validators=[group_name_validator], verbose_name=_("Name"))
    # acronym = models.CharField(max_length=3, validators=[validate_length], unique=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, null=True, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.center.ticker}_{self.name}"


class Invite(models.Model):
    group = models.OneToOneField(CgGroup, on_delete=models.CASCADE)
    code = models.CharField(max_length=64, unique=True, default=get_random_string(64))
    created = models.DateTimeField(auto_now_add=True)

    @property
    def expired(self):
        return False

    def __str__(self):
        return f"Invite to join {self.group}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(CgGroup, null=True, on_delete=models.SET_NULL)
    score = models.IntegerField(default=0)
    phone = models.CharField(max_length=10, validators=[validate_length], verbose_name=_("Phone Number"))

    def __str__(self):
        return f"Profile of {self.user.username}"


class Message(models.Model):
    title_he = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)

    description_he = models.TextField()
    description_en = models.TextField()

    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.title_en} ({self.date})"

    def save(self, *args, **kwargs):
        return super(Message, self).save(*args, **kwargs)
