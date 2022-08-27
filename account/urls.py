from django.urls import path
from . import views
from django.contrib.auth import views as authView

urlpatterns = [
    # register
    path("register/", views.register, name="register"),
    path("login/", authView.LoginView.as_view(), name="login"),
    path("logout/", authView.LogoutView.as_view(), name="logout"),
    path("change_password/", authView.PasswordChangeView.as_view(), name="password_change"),
    path("password_change_done/", authView.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password_reset/', authView.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset_done/", authView.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/", authView.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password_reset_complete/", authView.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    path('dashboard/edit_info/', views.edit_info, name="edit_info"),
    path("change_theme/", views.change_theme, name="change_theme"),
]
