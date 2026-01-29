from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (LoginView, RegistrationView, ActivationView,
                    ChangePasswordView, ForgotPasswordSendActivationCodeView,
                    ForgotPasswordCompleteView, ProfileMyView, ProfileUserView, ListUsersView,
                    BannedListUsersView, GoogleAuthorizationAPIView, GoogleLoginAPIView,
                    SendReviewAPIView)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login-google/', GoogleLoginAPIView.as_view(), name='login-google'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('register-google/', GoogleAuthorizationAPIView.as_view(), name='register-google'),

    path('activation_email/', ActivationView.as_view(), name='activation_email'),
    path('change_pass/', ChangePasswordView.as_view()),

    path('forgot_pass_send_activation_code/', ForgotPasswordSendActivationCodeView.as_view(),
         name='forgot_pass_send_activation_code'),
    path('forgot_pass_complete/', ForgotPasswordCompleteView.as_view(), name='forgot_pass_complete'),

    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileMyView.as_view(), name="profile"),
    path('profile/<int:id_user>/', ProfileUserView.as_view(), name="profile-user"),
    path('list/', ListUsersView.as_view(), name="list"),
    path('banned_list/', BannedListUsersView.as_view(), name="banned_list"),

    path('send_review/', SendReviewAPIView.as_view(), name="send_review"),
]
