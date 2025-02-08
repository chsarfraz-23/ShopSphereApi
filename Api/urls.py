from django.urls import path

from Api.views import UserSignUp

app_name = "Api"

urlpatterns = [
    path("signup/", UserSignUp.as_view()),
]