from django.db import models

from common.models import AbstractModel
from .validators import company_id_validator, person_id_validator


class Company(AbstractModel):
    user = models.OneToOneField(
        "access.User",
        on_delete=models.CASCADE,
        related_name="company_profile",
        null=False,
    )

    name = models.CharField(max_length=128, unique=True, null=False)
    vat = models.IntegerField(validators=[company_id_validator])
    phone = models.IntegerField()

    class Meta:
        verbose_name_plural = "Companies"


class Person(AbstractModel):
    user = models.OneToOneField(
        "access.User",
        on_delete=models.CASCADE,
        related_name="person_profile",
        null=False,
    )

    name = models.CharField(max_length=128, null=False)
    vat = models.IntegerField(validators=[person_id_validator])
    phone = models.IntegerField()

    class Meta:
        verbose_name_plural = "People"
