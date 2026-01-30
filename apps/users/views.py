import requests
from django.core.files.base import ContentFile
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed

from apps.announcement.models import Announcement
from apps.announcement.serializers import UserViewSerializer
from apps.complaint.models import Saved
from apps.users.models import MyUser
from apps.users.serializers import UserSerializer, LoginSerializer, ActivationSerializer, ChangePasswordSerializer, \
    ForgotPasswordSerializer, ForgotPasswordCompleteSerializer, ProfileSerializer, UserProfileUpdateSerializer, \
    AuthorizationServiceSerializer, LoginServiceSerializer, SendReviewSerializer

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from thailand_bazar.logic.send_email import send_email_gift, send_email_to_support


class RegistrationView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = MyUser.objects.create_user(
                full_name=request.data['full_name'],
                email=request.data['email'],
                phone_number=request.data['phone_number'],
                password=request.data['password'],
            )
            user.save()
            user.create_activation_code()
            user.send_activation_email()
            send_email_gift(user)

            saved = Saved.objects.create(
                user=user
            )
            saved.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class ActivationView(APIView):
    serializer_class = ActivationSerializer

    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response('Account successfully activated', status=200)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.set_new_password()
            return Response('Password successfully changed')
        else:
            return Response(serializer.errors, status=400)


class ForgotPasswordSendActivationCodeView(APIView):
    serializer_class = ForgotPasswordCompleteSerializer
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_code()
            return Response('Вам выслан код верификации')


class ForgotPasswordCompleteView(APIView):
    serializer_class = ForgotPasswordCompleteSerializer
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordCompleteSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Пароль успешно обновлён')


class ProfileMyView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve user profile details including announcements or update.",
        responses={200: ProfileSerializer()}
    )
    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileUserView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve user profile details including announcements.",
        responses={200: ProfileSerializer()}
    )
    def get(self, request, id_user):
        user = get_object_or_404(MyUser, id=id_user)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)


class ListUsersView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Список пользователей",
        responses={200: UserViewSerializer()}
    )
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 50

        users = MyUser.objects.filter(is_active=True)
        result_page = paginator.paginate_queryset(users, request)
        users_serializer = UserViewSerializer(instance=result_page, many=True)

        return paginator.get_paginated_response(users_serializer.data)


class BannedListUsersView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Список пользователей",
        responses={200: UserViewSerializer()}
    )
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 50

        users = MyUser.objects.filter(is_active=False)
        result_page = paginator.paginate_queryset(users, request)
        users_serializer = UserViewSerializer(instance=result_page, many=True)

        return paginator.get_paginated_response(users_serializer.data)


class GoogleAuthorizationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = AuthorizationServiceSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        token = serializer.data["token"]
        try:
            info_user: dict = id_token.verify_oauth2_token(token, google_requests.Request())
        except ValueError:
            raise AuthenticationFailed(detail="Bad token Google", code=403)
        with transaction.atomic():
            print(info_user)
            if MyUser.objects.filter(email=info_user["email"]).first():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user = MyUser.objects.create(
                email=info_user["email"],
                full_name=info_user["name"]
            )
            user.is_active = True
            user.create_activation_code()
            user.send_activation_email()

            user.save()

            avatar_url = info_user.get("picture")
            if avatar_url:
                response = requests.get(avatar_url)
                if response.status_code == 200:
                    user.avatar.save(f"{user.email}_avatar.jpg", ContentFile(response.content))

            saved = Saved.objects.create(
                user=user
            )
            saved.save()
            return Response(status=status.HTTP_201_CREATED)


class GoogleLoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = AuthorizationServiceSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        token = serializer.data["token"]
        try:
            info_user: dict = id_token.verify_oauth2_token(token, google_requests.Request())
        except ValueError:
            raise AuthenticationFailed(detail="Bad token Google", code=403)
        with transaction.atomic():
            if MyUser.objects.filter(email=info_user["email"]).first():
                user = MyUser.objects.get(email=info_user["email"])
                login_serializer = LoginServiceSerializer(data={
                    "email": user.email
                })
                login_serializer.is_valid(raise_exception=True)
                return Response(login_serializer.validated_data, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_404_NOT_FOUND)


class SendReviewAPIView(APIView):
    serializer_class = SendReviewSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SendReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_email_to_support(serializer.data)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


