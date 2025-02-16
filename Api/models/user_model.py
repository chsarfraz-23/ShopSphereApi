from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from shortuuid.django_fields import ShortUUIDField

from Api.models.abstract_models import AuditTrailDateTimeOnly


class User(AbstractUser, AuditTrailDateTimeOnly):
    id = ShortUUIDField(primary_key=True)
    pic = models.ImageField(upload_to="profile_images", null=True, blank=True)
    phone_number = PhoneNumberField(max_length=20, null=True, blank=True, region="PK")
    cnic = models.CharField(max_length=244, null=True, blank=True)

    def __str__(self):
        return f"Username={self.username}, email={self.email}"
