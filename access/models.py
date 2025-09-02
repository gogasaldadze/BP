# models.py
from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from common.models import AbstractModel


class UserManager(BaseUserManager):
    """Custom user manager with clean separation of concerns."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError("Email address is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create a regular user."""
        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create a superuser."""
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, AbstractModel):
    """Custom user model with email as username field."""

    class UserType(models.TextChoices):
        """User type choices with clear naming."""

        COMPANY = "company", "Company"
        PERSON = "person", "Person"

    # Core fields
    email = models.EmailField(
        unique=True, db_index=True, help_text="Email address used for authentication"
    )

    name = models.CharField(
        max_length=150, blank=True, help_text="Display name for the user"
    )

    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        help_text="Type of user account",
        blank=True,
        null=True,
    )

    # Permission fields
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )

    is_admin = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into the admin site.",
    )

    # Django auth requirements
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "auth_user"

    def __str__(self):
        return f"{self.email}"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

        if not self.is_admin and not self.user_type:
            raise ValidationError("User type is required for non-admin users")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # Permission methods (required by Django)
    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    # Business logic methods
    @property
    def is_company(self):
        return self.user_type == self.UserType.COMPANY

    @property
    def is_person(self):
        return self.user_type == self.UserType.PERSON

    def get_profile(self):
        if self.is_company:
            return getattr(self, "company_profile", None)
        elif self.is_person:
            return getattr(self, "person_profile", None)
        return None


# # services.py - Business logic separated from models
# from django.db import transaction
# from django.core.exceptions import ValidationError


# class UserService:
#     """Service class for user-related business logic."""

#     @staticmethod
#     @transaction.atomic
#     def create_user_with_profile(email, password, user_type, profile_data):
#         """Create user with associated profile in a single transaction."""
#         # Import here to avoid circular imports
#         from content.models import Company, Person

#         # Validate user type
#         if user_type not in [User.UserType.COMPANY, User.UserType.PERSON]:
#             raise ValidationError(f"Invalid user type: {user_type}")

#         try:
#             # Create user
#             user = User.objects.create_user(
#                 email=email, password=password, user_type=user_type
#             )

#             # Create associated profile
#             if user_type == User.UserType.COMPANY:
#                 Company.objects.create(user=user, **profile_data)
#             else:
#                 Person.objects.create(user=user, **profile_data)

#             return user

#         except Exception as e:
#             # Transaction will be rolled back automatically
#             raise ValidationError(f"Failed to create user: {str(e)}")

#     @staticmethod
#     def get_user_with_profile(user_id):
#         """Get user with their profile data."""
#         try:
#             user = User.objects.select_related().get(id=user_id)
#             profile = user.get_profile()
#             return user, profile
#         except User.DoesNotExist:
#             return None, None


# # signals.py - Event handling
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model

# User = get_user_model()


# @receiver(post_save, sender=User)
# def user_post_save(sender, instance, created, **kwargs):
#     """Handle user creation events."""
#     if created:
#         # Log user creation, send welcome email, etc.
#         print(f"New user created: {instance.email}")


# @receiver(post_delete, sender=User)
# def user_post_delete(sender, instance, **kwargs):
#     """Handle user deletion events."""
#     # Cleanup related data, log deletion, etc.
#     print(f"User deleted: {instance.email}")


# # admin.py - Clean admin interface
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     """Custom user admin with proper field organization."""

#     list_display = ("email", "name", "user_type", "is_active", "is_admin", "created_at")
#     list_filter = ("user_type", "is_active", "is_admin", "created_at")
#     search_fields = ("email", "name")
#     ordering = ("email",)

#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         ("Personal info", {"fields": ("name", "user_type")}),
#         (
#             "Permissions",
#             {"fields": ("is_active", "is_admin"), "classes": ("collapse",)},
#         ),
#         (
#             "Important dates",
#             {
#                 "fields": ("last_login", "created_at", "updated_at"),
#                 "classes": ("collapse",),
#             },
#         ),
#     )

#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("email", "user_type", "password1", "password2"),
#             },
#         ),
#     )

#     readonly_fields = ("created_at", "updated_at", "last_login")


# # views.py - Clean API views
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny
# from .services import UserService
# from .serializers import UserRegistrationSerializer


# class UserRegistrationView(APIView):
#     """User registration endpoint with clean separation."""

#     permission_classes = [AllowAny]
#     serializer_class = UserRegistrationSerializer

#     def post(self, request):
#         """Register a new user with profile."""
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         try:
#             user = UserService.create_user_with_profile(
#                 email=serializer.validated_data["email"],
#                 password=serializer.validated_data["password"],
#                 user_type=serializer.validated_data["user_type"],
#                 profile_data=serializer.validated_data["profile_data"],
#             )

#             return Response(
#                 {"message": "User created successfully", "user_id": user.id},
#                 status=status.HTTP_201_CREATED,
#             )

#         except ValidationError as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
