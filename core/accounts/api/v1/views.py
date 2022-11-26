from rest_framework import generics, status
from rest_framework.response import Response
from .serializer import (
    RegistrationSerializer,
    CastumAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangPasswordSerializer,
    ProfileApiViewSerializer,
    ActivationResendApiviewSerializer,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from ...models import Profile
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from .utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
    DecodeError,
)

User = get_user_model()


class RegistrationApiview(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "as_akh@yahoo.com",
                to=[email],
            )
            # TODO: Add more useful commands here.
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CastumAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangPasswordApiview(generics.GenericAPIView):
    serializer_class = ChangPasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password change successfully"},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileApiViewSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    # class TestEmailSend(APIView):

    #     def get(self, request, *args, **kwargs):
    #         self.email = "a1@k1.com"
    #         user_obj = get_object_or_404(User, email=self.email)
    #         token = self.get_tokens_for_user(user_obj)
    #         email_obj = EmailMessage(
    #             "email/hello.tpl",
    #             {"token": token},
    #             "as_akh@yahoo.com",
    #             to=[self.email],
    #         )
    #         # TODO: Add more useful commands here.
    #         print('email_obj')
    #         email_obj.send()
    #         # EmailThread(email_obj).start()

    #         return Response("email send")

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationApiview(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"detaile": "token has ben expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"detaile": "token invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DecodeError:
            return Response(
                {"detaile": "token invalid not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # decode user_id
        # object user
        # is-verified=True
        # if token not valied
        # response ok
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response(
                {"detaile": "this account has alradey verified "},
                status=status.HTTP_200_OK,
            )
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"detaile": "verified is sucsessfully"}, status=status.HTTP_200_OK
        )


class ActivationResendApiview(generics.GenericAPIView):
    serializer_class = ActivationResendApiviewSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendApiviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "as_akh@yahoo.com",
            to=[user_obj.email],
        )
        # TODO: Add more useful commands here.
        EmailThread(email_obj).start()
        return Response(
            {"detaile": "user activation email sending"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
