from openai import OpenAI
from rest_framework import serializers

from Api.models import User, ProductType, Product, ProductImage
from Api.models.api_models import DeepSeekRequestResponseModel
from Backend_Api import settings


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if User.objects.filter(username__iexact=validated_data["username"]).exists():
            raise serializers.ValidationError(f"User with this name: '{validated_data["username"]}' already exists.")
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class AuthUserActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "pic"
        ]

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if request and request.user != instance.user:
            raise serializers.ValidationError("You are not allowed to update this data.")
        for attrs, value in validated_data.items():
            setattr(instance, attrs, value)
        return instance


class ProductTypeSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = ProductType
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(required=True, queryset=ProductType.objects.all())
    product_images = serializers.PrimaryKeyRelatedField(required=False, many=True, allow_null=True,
                                                        queryset=ProductImage)
    is_active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "discount",
            "city",
            "state",
            "country",
            "address",
            "email",
            "phone_number",
            "is_active",
            "type",
            "product_images",
            "created_by",
            "modified_by",
            "created_at",
            "modified_at"
        ]

    def create(self, validate_data):
        validated_data = self.validated_data
        product_images = self.validated_data.pop("product_images", [])
        product = Product.objects.create(**validated_data)
        for product_image in product_images:
            product.images.add(product_image)
        product.save()
        return product


class ProductReadOnlySerializer(serializers.ModelSerializer):
    type = ProductTypeSerializer(read_only=True)
    images = ProductImageSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "discount",
            "city",
            "state",
            "country",
            "address",
            "email",
            "phone_number",
            "is_active",
            "type",
            "images",
        ]


class DeepSeekAPIViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeepSeekRequestResponseModel
        fields = "__all__"

    def create(self, validated_data):
        client = OpenAI(api_key=settings.DEEP_SEEK_API_KEY, base_url=settings.DEEP_SEEK_API_BASE_URL)
        query = validated_data["query"]
        response = client.chat.completions.create(
            model=settings.DEEP_SEEK_PROVIDER_MODEL_REFERENCE,
            messages=[{"role": "user", "content": query}],
            stream=False
        )
        answer = response.choices[0].message.content
        validated_data["answer"] = answer
        instance = super().create(validated_data)
        return instance

