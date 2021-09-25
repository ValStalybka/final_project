from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post, Comment


class PostListView(ListView):
    model = Post
    template_name = 'blog/all_posts.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'


class PostCreateView(CreateView):
    fields = ['title', 'text', 'author']
    model = Post
    template_name = 'blog/create_post.html'


class PostUpdateView(UpdateView):
    fields = ['title', 'text', 'author']
    model = Post
    template_name = 'blog/edit_post.html'


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:all_posts')






