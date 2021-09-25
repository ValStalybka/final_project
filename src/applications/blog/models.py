from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=225)
    text = models.TextField()
    likes = models.PositiveIntegerField(default=0, blank=True, null=True)
    dislikes = models.PositiveIntegerField(default=0, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('blog:post', kwargs={"pk": str(self.pk)})


class Comment(models.Model):
    title = models.CharField(max_length=225)
    text = models.TextField()
    likes = models.PositiveIntegerField(blank=True, null=True)
    dislikes = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['date']

    def __str__(self):
        return self.title
