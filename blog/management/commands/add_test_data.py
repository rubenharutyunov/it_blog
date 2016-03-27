import random
from django.core.management.base import BaseCommand
from blog.models import Comment, Post, Category, Tag
from users.models import User
from django.utils.text import slugify

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
            categories = []
            tags = []
            print("Adding categories")
            for i in range(random.randint(5,25)):
                categories.append(Category(title="Test category #%s" % i, description="desc %s" % i))
            for category in categories:
                    category.save()    
            print("Adding tags")  
            for i in range(random.randint(2,7)):
                tags.append(Tag(title="Test Tag #%s" % i)) 
            for tag in tags:
                    tag.save()    
            print(type(tags))              
            print("Adding test posts...")
            for i in range(random.randint(10,20)):
                posts.append(Post(title="Post #%s" % i, text="Text of post #%s" % i, slug=slugify("Text of post #%s" % i), author=admin_user, \
                    views=random.randint(1,999), likes=random.randint(1,999), category=random.choice(categories)))
            print("Adding comments")    
            for post in posts:
                post.save()
                post.tags.add(random.choice(tags),random.choice(tags))
                post.save()
                for i in range(random.randint(1,20)):
                    comments.append(Comment(post=post, text="Comment for %s #%s" % (post, i), author=admin_user, likes=random.randint(1,999)))      
            for comment in comments:
                comment.save()   
        else:
            print("Deleting")
            Post.objects.all().delete()
            Comment.objects.all().delete() 
            Category.objects.all().delete() 
            Tag.objects.all().delete()        
