from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from Api.models import ProductImage, ProductType, Product
from Api.models.user_model import User
from Api.serializers import UserSignUpSerializer, ProductImageSerializer, ProductTypeSerializer, \
    ProductReadOnlySerializer, ProductSerializer, AuthUserActionsSerializer


class UserSignUp(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh: RefreshToken = RefreshToken.for_user(user=user)
        return Response({"access": str(refresh), "refresh": str(refresh.access_token)})


class AuthUserActionsView(
    mixins.UpdateModelMixin,
    viewsets.ReadOnlyModelViewSet
):
    queryset = User.objects.all().order_by("-created_at")
    serializer_class = AuthUserActionsSerializer
    permission_classes = (IsAuthenticated,)


class ProductImageView(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all().order_by("-created_at")
    serializer_class = ProductImageSerializer
    permission_classes = (IsAuthenticated,)


class ProductTypeView(viewsets.ModelViewSet):
    queryset = ProductType.objects.all().order_by("-created_at")
    serializer_class = ProductTypeSerializer
    permission_classes = (IsAdminUser,)


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class_read_only = ProductReadOnlySerializer
    serializer_class_write_only = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return self.serializer_class_write_only
        return self.serializer_class_read_only


