from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy

from .views import ProfileUpdateView, ProfileDetailView, UserRegisterView, UserLogoutView, \
    UserPasswordChangeView, CustomLoginView, UserForgotPasswordView, UserPasswordResetConfirmView, \
    EmailConfirmationSentView, UserConfirmEmailView, EmailConfirmedView, EmailConfirmationFailedView, \
    ProfileDetailBlogsView, ProfileDetailNewsView, ProfileDetailArticlesView

urlpatterns = [
    path('user/<str:slug>/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('user/<str:slug>/articles/', ProfileDetailArticlesView.as_view(), name='profile_articles_list'),
    path('user/<str:slug>/blogs/', ProfileDetailBlogsView.as_view(), name='profile_blog_list'),
    path('user/<str:slug>/news/', ProfileDetailNewsView.as_view(), name='profile_news_list'),
    path('user/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('user/<str:slug>/password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),


    # path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    # path('password-reset/',
    #      PasswordResetView.as_view(
    #          template_name="account/password_reset_form.html",
    #          email_template_name="account/password_reset_email.html",
    #          success_url=reverse_lazy("password_reset_done")
    #      ),
    #      name='password_reset'),
    # path('password-reset/done/',
    #      PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"),
    #      name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/',
    #      PasswordResetConfirmView.as_view(
    #          template_name="account/password_reset_confirm.html",
    #          success_url=reverse_lazy("password_reset_complete")
    #      ),
    #      name='password_reset_confirm'),
    # path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"), name='password_reset_complete'),
]
