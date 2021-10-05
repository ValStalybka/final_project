from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from .forms import CommentForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like

User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = "blog/all_posts.html"

    def get_queryset(self):
        query = self.request.GET.get('keyword')
        if query:
            object_list = Post.objects.filter(
                Q(title__icontains=query) | Q(text__icontains=query)
            )
        else:
            object_list = Post.objects.all()
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head'] = "Writing stuff on the Internet has never been easier"
        context['title'] = "All Posts"
        return context


class PersonalPostListView(PostListView):
    model = User
    template_name = "blog/all_posts.html"

    def get_queryset(self):
        qs = User.objects.get(id=self.kwargs.get("pk"))
        return qs.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Posts"
        return context


class LikedPostsListView(PostListView):
    model = Like
    template_name = "blog/all_posts.html"

    def get_queryset(self):
        return Post.objects.filter(likes=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Liked Posts"
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head'] = "Enjoy you reading experience"
        current_post = Post.objects.get(id=self.kwargs.get("pk"))
        liked = False
        if current_post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['liked'] = liked
        context['comments'] = current_post.comments.all()
        context['form'] = CommentForm
        context['title'] = "Post"
        return context


class PostCreateView(CreateView):
    fields = ["title", "text"]
    model = Post
    template_name = "blog/create_post.html"

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            redirect_url = reverse_lazy("blog:signup")
            return HttpResponseRedirect(str(redirect_url))
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head"] = "Write your message to the world"
        context['title'] = "New Post"
        return context


class OwnerPostMixin:
    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise Http404()
        return super().get_queryset().filter(author=self.request.user)


class PostUpdateView(OwnerPostMixin, UpdateView):
    fields = ["title", "text"]
    model = Post
    template_name = "blog/edit_post.html"

    def get_success_url(self):
        url = reverse_lazy("blog:post", kwargs={"pk": self.kwargs["pk"]})
        return url

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head'] = "Take back everything you've said without any consequences"
        context['title'] = "Edit Post"
        return context


class PostDeleteView(OwnerPostMixin, DeleteView):
    model = Post
    template_name = "blog/delete_post.html"
    success_url = reverse_lazy("blog:all_posts")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head'] = "Are you sure you wanna delete this post?"
        context['title'] = "Delete Post"
        return context


class CommentCreateView(CreateView):

    form_class = CommentForm
    http_method_names = ["post"]
    model = Post

    def get_success_url(self):
        url = reverse_lazy("blog:post", kwargs={"pk": self.kwargs["pk"]})
        return url

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            redirect_url = reverse_lazy("blog:signup")
            return HttpResponseRedirect(str(redirect_url))
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.post = Post.objects.get(id=self.kwargs["pk"])
        obj.save()
        return super().form_valid(form)


class CommentUpdateView(OwnerPostMixin, UpdateView):
    model = Comment
    fields = ["text"]
    template_name = "blog/edit_comment.html"

    def get_success_url(self):
        url = reverse_lazy("blog:post", kwargs={"pk": self.request.POST.get("post_id")})
        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head'] = "Take back everything you've said without any consequences"
        context['title'] = "Edit Comment"
        return context


class CommentDeleteView(OwnerPostMixin, DeleteView):
    model = Comment
    template_name = "blog/delete_comment.html"

    def get_success_url(self):
        url = reverse_lazy("blog:post", kwargs={"pk": self.request.POST.get("post_id")})
        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head'] = "Are you sure you wanna delete this post?"
        context['title'] = "Delete Comment"
        return context


def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = False
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse_lazy("blog:post", args=[str(pk)]))
