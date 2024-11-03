from django.urls import path

from common.views import IndexView, UserLogin, UserLogout, UserRegistrationView

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", UserLogout.as_view(), name="logout"),
]
