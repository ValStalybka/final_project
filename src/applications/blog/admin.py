from django.contrib import admin

from .models import Comment
from .models import Post
from .models import Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', "title", 'text', 'date', 'author_id',)
    list_display_links = ('id', "title")
    search_fields = ("author", "title")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'date', 'post_id', 'author_id')
    list_display_links = ('id', )
    search_fields = ("author", )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
