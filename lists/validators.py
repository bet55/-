from rest_framework.exceptions import ValidationError


def validate_kp_id(field):
    if field is None:
        raise ValidationError('kp_id is required')


def validate_name(field):
    if field is None:
        raise ValidationError('Name is required')
