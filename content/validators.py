from django.core.validators import RegexValidator


company_id_validator = RegexValidator(
    regex=r"^\d{9}$", message="ID must be exactly 9 digits", code="invalid_id"
)


person_id_validator = RegexValidator(
    regex=r"^\d{11}$",
    message="Personal ID must be exactly 11 digits",
    code="invalid_id",
)
