from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, mixins, views, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from Api.filters import CartProductItemFilter
from Api.models import ProductImage, ProductType, Product
from Api.models.api_models import DeepSeekRequestResponseModel, CartProductItem
from Api.models.user_model import User
from Api.serializers import UserSignUpSerializer, ProductImageSerializer, ProductTypeSerializer, \
    ProductReadOnlySerializer, ProductSerializer, AuthUserActionsSerializer, DeepSeekAPIViewSerializer, \
    CartProductItemSerializer
from ShopSphereApi.pagination import IncludePageSizePagination


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


class ProductCartItemView(viewsets.ModelViewSet):  #ToDo: Testing remaining
    pagination_class = IncludePageSizePagination
    queryset = CartProductItem.objects.all().order_by("-created_at").select_related("product")
    serializer_class = CartProductItemSerializer
    filterset_class = CartProductItemFilter
    permission_classes = (IsAuthenticated,)


class DeepSeekApiView(views.APIView):
    pagination_class = IncludePageSizePagination()
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        start_time = datetime.now()
        serializer = DeepSeekAPIViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        end_time = datetime.now()
        instance.response_in_seconds = int((end_time - start_time).seconds)
        instance.save()
        return Response(DeepSeekAPIViewSerializer(instance).data, status=status.HTTP_201_CREATED)

    def get(self, request, pk=None):
        if not pk:
            queryset = DeepSeekRequestResponseModel.objects.all().order_by("-created_at")
            paginated_query_set = self.pagination_class.paginate_queryset(queryset, request)
            serializer = DeepSeekAPIViewSerializer(paginated_query_set, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)

        deepseek_request_response_model = get_object_or_404(DeepSeekRequestResponseModel, id=pk)
        serializer = DeepSeekAPIViewSerializer(deepseek_request_response_model)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


