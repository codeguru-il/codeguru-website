from __future__ import annotations

from os.path import join
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.db.models.signals import pre_init
from django.utils import timezone

from codeguru.models import CgGroup, Competition
from war.storage import get_survivor_path, submissions_storage
from website.settings import (
    SURVIVOR_SIGNATURE_ENABLED,
    SURVIVOR_SIGNATURE_GAP,
    SURVIVOR_SIGNATURE_OFFSET,
    SURVIVOR_SIGNATURE_VALUE,
)


class Challenge(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    required_riddles = models.ManyToManyField("Riddle", symmetrical=False, blank=True)

    class Meta:
        abstract = True

    @property
    def active(self):
        return self.start_date <= timezone.now() <= self.end_date

    def get_my_model_name(self):
        return self._meta.model_name

    def __str__(self):
        return "[{competition}] {start}~{end}: {title}".format(
            competition=self.competition,
            start=self.start_date.strftime("%Y-%m-%d"),
            end=self.end_date.strftime("%Y-%m-%d"),
            title=self.title,
        )


def format_survivor_name(entry, survivor_index: int, is_binary: bool):
    return f"{entry.group.center.ticker}_{entry.group.name}{survivor_index}" + ("" if is_binary else ".asm")


def war_directory_path(instance, is_binary: bool) -> str:
    if instance.group is None:
        return join("wars", "zombies", str(instance.war.id), uuid4().hex)
    name = format_survivor_name(instance, instance.warrior_file_idx, is_binary)

    return get_survivor_path(instance.war.id, name)


def riddle_directory_path(instance, filename):
    return join("riddles", str(instance.riddle.id), str(instance.group.id), "solution.zip")


def bin_max(value):
    filesize = value.size
    if filesize > 512:
        raise ValidationError("Too large.")
    else:
        return value


class SurvivorMachineCodeValidator:
    """
    Validates the machine code submitted for a survivor.

    Ensures that a file submitted for a survivor is not empty.
    If signature is required for the relevant competition,
    this validator also verifies the file matches the signature
    """

    def __init__(self, competition: Competition) -> None:
        self.signature_enabled = competition.survivor_signature_enabled
        self.signature_gap = competition.survivor_signature_gap
        self.signature_offset = competition.survivor_signature_offset
        self.signature_byte = competition.survivor_signature_value

    def __call__(self, value):
        machine_code = value.file.read()
        if not machine_code:
            raise ValidationError("Survivor may not be empty.")

        if not self.is_valid_signature(machine_code):
            raise ValidationError("Invalid signature.")

        return value

    def is_valid_signature(self, machine_code) -> bool:
        if not self.signature_enabled:
            # No signature check needed
            return True

        for i, byte in enumerate(machine_code):
            if i % self.signature_gap == self.signature_offset and not byte == self.signature_byte:
                return False

        return True


def asm_max(value):
    filesize = value.size
    if filesize > 1024**2:
        raise ValidationError("Too large.")
    else:
        return value


def asm_surv_upload(instance, _):
    return war_directory_path(instance, False)


def bin_surv_upload(instance, _):
    return war_directory_path(instance, True)


class Riddle(Challenge):
    pass


class War(Challenge):
    amount_of_survivors = models.PositiveIntegerField(default=2, validators=[MinValueValidator(1)])
    zombie_mode = models.BooleanField(default=False)
    required_wars = models.ManyToManyField("self", symmetrical=False, blank=True)


class Survivor(models.Model):
    group = models.ForeignKey(CgGroup, null=True, editable=False, on_delete=models.CASCADE)
    war = models.ForeignKey(War, null=True, on_delete=models.CASCADE)
    asm_file = models.FileField(null=True, upload_to=asm_surv_upload, validators=[asm_max], storage=submissions_storage)
    bin_file = models.FileField(upload_to=bin_surv_upload, validators=[bin_max], storage=submissions_storage)
    result = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [CheckConstraint(check=Q(result__gte=0.0), name="positive_result")]


def warrior_file_idx_modifier(sender, **kwargs):
    if kwargs.get("kwargs").get("warrior_file_idx"):
        sender.warrior_file_idx = kwargs.get("kwargs").pop("warrior_file_idx")


pre_init.connect(warrior_file_idx_modifier, Survivor)


class RiddleSolution(models.Model):
    riddle = models.ForeignKey(Riddle, on_delete=models.CASCADE)
    group = models.ForeignKey(CgGroup, null=True, on_delete=models.CASCADE)
    riddle_solution = models.FileField(
        upload_to=riddle_directory_path,
        storage=submissions_storage,
        validators=[FileExtensionValidator(allowed_extensions=["zip"])],
    )
    upload_date = models.DateTimeField(auto_now_add=True)
