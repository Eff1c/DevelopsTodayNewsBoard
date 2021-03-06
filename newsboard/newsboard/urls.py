from django.urls import path

from .views import PostViewSet, PostDetail, CommentViewSet, \
    CommentDetail, UpvoteView, DownvoteView


post_list = PostViewSet.as_view({"get": "list", "post": "create"})

comment_list = CommentViewSet.as_view({"get": "list", "post": "create"})


urlpatterns = [
    path("api/posts/", post_list),
    path("api/posts/<int:post_id>/comments/", comment_list),
    path("api/posts/<int:post_id>/", PostDetail.as_view()),
    path(
        "api/posts/<int:post_id>/comments/<int:comment_id>/",
        CommentDetail.as_view()
    ),
    path("api/posts/<int:post_id>/upvote/", UpvoteView.as_view()),
    path("api/posts/<int:post_id>/downvote/", DownvoteView.as_view()),
]
