from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interact.views import like_view, follow_view, comment_view

router = DefaultRouter()
# router.register(r'like', like_view.LikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('follow', follow_view.FollowListView.as_view({'post': 'create', 'delete': 'destroy'})),
    path('<int:post_id>/comments', comment_view.CommentView.as_view(), name='comment_list'),
    path('<int:post_id>/comments/<int:pk>', comment_view.CommentObjectView.as_view(), name='comment_object_view'),
    path('<int:post_id>/subcomments/<int:comment_ref_id>', comment_view.SubCommentListView.as_view()),
    path(
        '<int:post_id>/<str:like_or_dislike>',
        like_view.LikeViewSet.as_view({'get': 'list', 'post': 'create'}),
        name="like_view",
    ),
    path(
        '<int:post_id>/<str:like_or_dislike>/<int:owner_id>',
        like_view.LikeViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}),
    )
]
