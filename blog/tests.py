from django.test import TestCase
from blog.models import Post, Comment
from django.contrib.auth.models import User

class PostTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='user1')
        Post.objects.create(text="test", title="test_title", author=user)

    def test_post_comments(self):  
        user = User.objects.get(username='user1')  
        test_post = Post.objects.get(title="test_title")
        comment1 = Comment.objects.create(text="test", post=test_post, author=user)
        comment2 = Comment.objects.create(text="test2", post=test_post, author=user)
        self.assertEqual(comment1.post, test_post)
        self.assertEqual(comment1.author, user)
        self.assertEqual(comment2.post, test_post)
        self.assertEqual(comment2.author, user)

        self.assertEqual(comment1.post, comment2.post)
        self.assertEqual(comment1.author, comment2.author)

        self.assertSequenceEqual(test_post.comment_set.all(), [comment1, comment2])
