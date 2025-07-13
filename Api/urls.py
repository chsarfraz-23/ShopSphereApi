from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Api.views import UserSignUp, ProductImageView, ProductTypeView, ProductView, AuthUserActionsView, \
    ProductCartItemView

app_name = "Api"

router = DefaultRouter()
router.register(r"auth-user-actions", AuthUserActionsView, basename="auth-user-action")
router.register(r"product-images", ProductImageView, basename="product-image")
router.register(r"product-types", ProductTypeView, basename="product-type")
router.register(r"products", ProductView, basename="product")
router.register("cart-product-items", ProductCartItemView, basename="cart-product-items")

urlpatterns = [
    path("signup/", UserSignUp.as_view()),
    path("", include(router.urls))
]
