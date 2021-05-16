
from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('personal/edit', views.edit_personal_info, name="personal_info_edit")
]
