from rest_framework import serializers

from Api.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(email=validated_data["email"], username=validated_data["username"])
        if User.objects.filter(username__iexact=validated_data["username"]).exists():
            raise serializers.ValidationError(f"User with this name: '{validated_data["username"]}' already exists.")
        user.set_password(validated_data["password"])
        user.save()
        return user

