from django.db import transaction
from django.core.exceptions import ValidationError
from content.models import Company, Person


class Service:
    @transaction.atomic
    def create_user_with_profile(email, password, user_type, profile_data):
        from access.models import User

        user = User.objects.create_user(
            email=email, password=password, user_type=user_type
        )

        if user_type not in [User.UserType.COMPANY, User.UserType.PERSON]:
            raise ValidationError(f"Invalid user type: {user_type}")

        try:
            user = User.objects.create_user(
                email=email, password=password, user_type=user_type
            )

            if user.user_type == User.UserType.COMPANY:
                Company.objects.create(user=user, **profile_data)

            if user.user_type == User.UserType.PERSON:
                Person.objects.create(user=user, **profile_data)

        except Exception as e:
            raise ValidationError(f"Failed to create user: {str(e)}")
