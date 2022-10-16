from django.urls import path

from . import views

urlpatterns = [
    path("login", views.UserLoninView.as_view(), name="login"),
    path("logout", views.UserLogoutView.as_view(), name="logout"),
    path('register', views.UserRegisterView.as_view(), name="register"),
    path('home', views.HomeView.as_view(), name="home")
]
