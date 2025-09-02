from django.db import models

from common.models import AbstractModel
from .validators import company_id_validator, person_id_validator

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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


class Product(AbstractModel):
    class CategoryType(models.TextChoices):
        BOX = "box", "Box"
        PAPER = "paper", "Paper"
        OTHER = "other", "Other"

    name = models.CharField(max_length=128)
    description = models.TextField()
    category = models.CharField(max_length=12, choices=CategoryType.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(blank=True, null=True, upload_to="media/products/")


class Order(AbstractModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELED = "canceled", "Canceled"

    customer_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    customer_object_id = models.PositiveIntegerField()
    customer = GenericForeignKey("customer_content_type", "customer_object_id")

    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.PENDING
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


class OrderItem(AbstractModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="order_items",
        null=True,
        blank=True,
    )
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = [
            "order",
            "product",
        ]
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
