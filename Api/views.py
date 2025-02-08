from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from Api.models.user_model import User
from Api.serializers import UserSignUpSerializer


class UserSignUp(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh: RefreshToken = RefreshToken.for_user(user=user)
        return Response({"access": str(refresh), "refresh": str(refresh.access_token)})

