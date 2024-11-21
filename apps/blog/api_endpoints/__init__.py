from rest_framework import routers

from .blog import (
    PostViewSet,
    PostCommentViewSet,
    PostCommentLikeViewSet,
    PostLikeViewSet,
    PostDislikeViewSet,
)

router = routers.DefaultRouter()
router.register("post", PostViewSet, basename="post")
router.register("post_comment", PostCommentViewSet, basename="post-comment")
router.register(
    "post_comment_like", PostCommentLikeViewSet, basename="post-comment-like"
)
router.register("post_like", PostLikeViewSet, basename="post-like")
router.register("post_dislike", PostDislikeViewSet, basename="post-dislike")
