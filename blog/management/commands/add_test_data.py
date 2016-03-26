import random
from django.core.management.base import BaseCommand
from blog.models import Comment, Post
from django.contrib.auth.models import User

class Command(BaseCommand):
    def add_arguments(self, parser):
         parser.add_argument('--remove',
            action='store_true',
            dest='remove',
            default=False)

    def handle(self, *args, **options):
        if not options['remove']:
            admin_user = User.objects.get(id=1)
            posts = []
            comments = []
            print("Adding test posts...")
            for i in range(random.randint(10,20)):
                posts.append(Post(title="Post #%s" % i, text="Text of post #%s" % i, author=admin_user, views=random.randint(1,999), likes=random.randint(1,999)))
            print("Adding comments")    
            for post in posts:
                post.save()
                for i in range(random.randint(1,20)):
                    comments.append(Comment(post=post, text="Comment for %s #%s" % (post, i), author=admin_user, likes=random.randint(1,999)))      
            for comment in comments:
                comment.save()   
        else:
            print("Deleting")
            posts = Post.objects.all().delete()
            comments = Comment.objects.all().delete()         