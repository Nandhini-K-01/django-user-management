from django.urls import path 
from .views import RegisterView, LoginView, UserView, LogoutView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="drfregister"),
    path("login/", LoginView.as_view(), name="drflogin"),
    path("user/", UserView.as_view(), name="user"),
    path("logout/", LogoutView.as_view(), name="logout")
]