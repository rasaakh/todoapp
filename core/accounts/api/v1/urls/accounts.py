from django.urls import path
from .. import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path(
        "registeration/",
        views.RegistrationApiview.as_view(),
        name="registration",
    ),
    # path("test-email/", views.TestEmailSend.as_view(), name="test"),
    # activation
    path(
        "activation/confirm/<str:token>",
        views.ActivationApiview.as_view(),
        name="activation",
    ),
    # resend activation
    path(
        "activation/resend/",
        views.ActivationResendApiview.as_view(),
        name="activation-resend",
    ),
    # change password
    path(
        "change-password/",
        views.ChangPasswordApiview.as_view(),
        name="change-password",
    ),
    # login and logout by Token
    path("token/login/", views.CustomAuthToken.as_view(), name="token-login"),
    path(
        "token/logout/",
        views.CustomDiscardAuthToken.as_view(),
        name="token-logout",
    ),
    # jwt authentication
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
