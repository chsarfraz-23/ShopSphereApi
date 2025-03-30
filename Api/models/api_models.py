from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from shortuuid.django_fields import ShortUUIDField

from Api.models import AuditTrailModel


class ProductType(AuditTrailModel):
    id = ShortUUIDField(primary_key=True, db_index=True, editable=False)
    name = models.CharField(max_length=288)
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"ProductType(id={self.id} , name={self.id})"


class ProductImage(AuditTrailModel):
    id = ShortUUIDField(primary_key=True, db_index=True, editable=False)
    image = models.ImageField(upload_to="product_images", null=True, blank=True)

    def __str__(self):
        return f"ProductImage(id={self.id})"


class Product(AuditTrailModel):
    id = ShortUUIDField(primary_key=True, db_index=True, editable=False)
    name = models.CharField(max_length=288)
    price = models.CharField(max_length=288)
    discount = models.CharField(max_length=288, null=True, blank=True)
    city = models.CharField(max_length=288)
    state = models.CharField(max_length=288)
    images = models.ManyToManyField(ProductImage, related_name="product")
    country = models.CharField(max_length=288)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=288, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, region="PK")
    is_active = models.BooleanField(default=True)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return f"Product(id={self.id}, type={self.name})"


class DeepSeekRequestResponseModel(AuditTrailModel):
    id = ShortUUIDField(primary_key=True, editable=False, db_index=True)
    query = models.TextField()
    answer = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    response_in_seconds = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"DeepSeekRequestResponseModel(id={self.id}, query={self.query})"






