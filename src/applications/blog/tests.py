from django.test import TestCase
from .models import Comment, Post
from django.urls import reverse
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


class PostListViewTest(TestCase):

    def test_view_url_not_exists_at_desired_location(self):
        resp = self.client.get('/blog/post/post_id/')
        self.assertEqual(resp.status_code, 404)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('blog:all_posts'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('blog:all_posts'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'blog/all_posts.html')


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Comment.objects.create(text="some comment text", post_id=2, author_id=2)
        Comment.objects.create(text=" ", post_id=123, author_id=22)
        Comment.objects.create(text="Sample_with_numbers123", post_id=1, author_id=21)
        Comment.objects.create(text="!@$%#@", post_id=3, author_id=6)




