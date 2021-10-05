from django.urls import path

from ..registration.views import SignUpView

from .apps import BlogConfig
from .views import *


app_name = BlogConfig.label

urlpatterns = [
    path("", PostListView.as_view(), name="all_posts"),
    path("<int:pk>/", PostDetailView.as_view(), name="post"),
    path("new/", PostCreateView.as_view(), name="create_post"),
    path("<int:pk>/edit/", PostUpdateView.as_view(), name="edit_post"),
    path("delete/<int:pk>/", PostDeleteView.as_view(), name="delete_post"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("<int:pk>/comment/", CommentCreateView.as_view(), name="add_comment"),
    path("comment/edit/<int:pk>/", CommentUpdateView.as_view(), name="edit_comment"),
    path("comment/delete/<int:pk>/", CommentDeleteView.as_view(), name="delete_comment"),
    path("user/<int:pk>/", PersonalPostListView.as_view(), name="user_posts"),
    path("<int:pk>/like", like_view, name="like"),
    path("user/liked/<int:pk>", LikedPostsListView.as_view(), name="liked_posts")

]
