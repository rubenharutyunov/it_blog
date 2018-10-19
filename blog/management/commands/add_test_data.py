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

    def handle(self, remove, *args, **options):
        if not remove:
            admin_user = User.objects.get(id=1)
            posts = []
            comments = []
            categories = []
            tags = []
            print("Adding categories")
            for i in range(random.randint(5,25)):
                categories.append(Category(title="Test category #%s" % i, description="desc %s" % i, slug="test-cat-%s" % i))
            for category in categories:
                    category.save()
            print("Adding tags")
            for i in range(random.randint(50,150)):
                tags.append(Tag(title="Test Tag #%s" % i, slug="test-tag-%s" % i))
            for tag in tags:
                    tag.save()
            print(type(tags))
            print("Adding test posts...")
            for i in range(random.randint(10,20)):
                image = 'http://ih1.redbubble.net/image.175848241.2112/flat,800x800,075,f.jpg'
                post_text = '<p><img alt="" src="%s" style="float:left; height:200px; margin-left:10px; margin-right:10px; width:200px" />Lorem ipsum dolor sit amet, consectetur adipiscing elit. In suscipit varius nunc, et pretium velit faucibus sed. Sed varius lobortis urna, id aliquet tortor vehicula sit amet. Nulla molestie purus non lacus porttitor semper. Donec vehicula odio at sapien scelerisque, vel egestas orci ultrices. Curabitur in condimentum felis. Praesent dignissim orci interdum iaculis finibus. Suspendisse potenti. Sed maximus vulputate porta. Praesent interdum blandit nulla, quis laoreet leo fringilla quis. Cras nec sapien feugiat, interdum enim et, iaculis elit. Nunc gravida mauris non nulla imperdiet rutrum. Etiam dictum nisi vitae est pulvinar, a volutpat dui sagittis.</p> <p>In non pretium tortor, vel porttitor nibh. Nunc rhoncus lorem eu congue condimentum. Aliquam eu suscipit metus. Pellentesque sit amet augue nec eros dignissim condimentum nec mattis mauris. Praesent faucibus magna purus, a egestas sapien semper eget. Proin sapien dolor, accumsan vel congue sed, ornare vitae metus. In hac habitasse platea dictumst. Nunc sed nibh pellentesque, fermentum arcu non, scelerisque felis. Suspendisse massa mi, euismod et sollicitudin sit amet, placerat ornare arcu.</p> <p>Ut eget luctus nibh, non faucibus sapien. Nullam et metus luctus, aliquam sapien in, ullamcorper sapien. Cras vestibulum tellus eu velit blandit auctor. Vestibulum at scelerisque turpis, vitae porta urna. Integer laoreet diam ...</p>' % image
                posts.append(Post(title="Post #%s" % i, text=post_text, slug=slugify("Text of post #%s" % i), author=admin_user, \
                    views=random.randint(1,999), likes=random.randint(1,999), category=random.choice(categories)))
            print("Adding comments")
            for post in posts:
                post.save()
                for i in range(random.randint(3,11)): post.tags.add(random.choice(tags))
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
