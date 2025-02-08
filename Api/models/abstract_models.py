from django.db import models
from shortuuid.django_fields import ShortUUIDField


class AuditTrailDateTimeOnly(models.Model):
    id = ShortUUIDField(primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditTrailModel(AuditTrailDateTimeOnly):
    id = ShortUUIDField(primary_key=True)
    created_by = models.ForeignKey(
        "User",
        blank=True,
        null=True,
        related_name="%(class)s_created",
        on_delete=models.CASCADE,
    )
    modified_by = models.ForeignKey(
        "User",
        null=True,
        blank=True,
        related_name="%(class)s_modified",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
