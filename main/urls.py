from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('signup/', views.sign_up, name="signup"),
    path('posts/', views.create_post, name="create-post")
]