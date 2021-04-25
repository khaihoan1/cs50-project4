from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interact.views.like_view import LikeViewSet

router = DefaultRouter()
router.register(r'like', LikeViewSet)

urlpatterns = [
    path('', include(router.urls))
]
