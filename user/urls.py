from django.urls import path

from user import views

app_name = '[user]'
urlpatterns = [
    # path("login/", views.user_login, name="user_login"),
    path("login/", views.LoginView.as_view(), name="user_login"),
    # path("register/", views.user_register, name="user_register")
    path("register/", views.RegisterView.as_view(), name="user_register"),
    path("logout/", views.LogoutView.as_view(), name="user_logout"),
    path("profile/", views.ProfileView.as_view(), name="user_profile")
]
