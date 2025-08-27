from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from common.models import AbstractModel


class UserManager(BaseUserManager):

    def _create_user(self, password, **kwargs):
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password, **kwargs):
        kwargs["is_admin"] = False
        return self._create_user(password, **kwargs)

    def create_superuser(self, password, **kwargs):
        kwargs["is_admin"] = True
        return self._create_user(password, **kwargs)


class CustomUser(AbstractBaseUser, AbstractModel):

    email = models.EmailField(
        max_length=128, blank=True, null=True, unique=True, db_index=True
    )

    name = models.CharField(max_length=128, blank=True)
    password = models.CharField(max_length=128)

    is_active = models.BooleanField(
        help_text="Designates whether this user can access their account."
    )

    is_admin = models.BooleanField(
        help_text="designates whether the user can log into this admin site."
    )

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.name})"

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin and self.is_staff

    def has_module_perm(self, app_label):
        return self.is_active and self.is_admin

    def get_all_permissions(self, obj=None):
        return []
