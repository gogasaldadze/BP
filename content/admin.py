from django.contrib import admin
from .models import Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name", "category"]
    readonly_fields = ["id", "uuid", "created_at", "updated_at"]
    list_display = [
        "name",
        "category",
        "created_at",
    ]
