from django.urls import path
import users.views as views

urlpatterns = [
    path('',views.home, name="home_page"),
    path("login", views.user_login, name="login_page"),
    path("register",views.user_register, name="register_page"),
    path("profile", views.user_profile, name="profile_page"),
    path("logout", views.user_logout, name="logout_page"),
]