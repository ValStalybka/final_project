from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

User = get_user_model()


class CommonField(models.Model):
    text = models.TextField()
    date = models.DateField(auto_now_add=True, editable=True)

    @property
    def likes_number(self):
        return self.likes.all().count()

    class Meta:
        abstract = True


class Post(CommonField):
    title = models.CharField(max_length=225)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(User, blank=True, default=None, through="Like")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("blog:post", kwargs={"pk": str(self.pk)})


class Comment(CommonField):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-date"]

    def __str__(self):
        return self.text


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked")

    def __str__(self):
        return str(self.post)


