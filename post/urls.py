from django.urls import path
from .views import PostCreateView, PostDetailView, PostEditView, PostDeleteView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('create/', login_required(PostCreateView.as_view()), name="post_create"),
    path("<str:pk>/", PostDetailView.as_view(), name="post_detail"),
    path('edit/<str:pk>', PostEditView.as_view(), name="post_edit"),
    path('delete/<str:pk>', PostDeleteView.as_view(), name="post_delete")
]
