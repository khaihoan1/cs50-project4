from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interact.views import like_view, follow_view, comment_view

router = DefaultRouter()
router.register(r'like', like_view.LikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('follow/', follow_view.FollowListView.as_view()),
    # path('comment/', comment_view.CommentListView.as_view(), name='comment_list'),
    path('<int:post_id>/comments', comment_view.CommentListView.as_view(), name='comment_list'),
    path('<int:post_id>/comments/<int:pk>', comment_view.CommentObjectView.as_view(), name='comment_object_view')
]
