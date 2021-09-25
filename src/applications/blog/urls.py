from django.contrib import admin
from django.urls import path

from .apps import BlogConfig
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = BlogConfig.label


urlpatterns = [
    path('', PostListView.as_view(), name='all_posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='post'),
    path('new/', PostCreateView.as_view(), name='create_post'),
    path('edit/<int:pk>', PostUpdateView.as_view(), name='edit_post'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete_post')
]
