from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.conf import settings


def send_approved_email(post):
    user = post.author
    domain = Site.objects.get_current().domain
    link = "http://%s/post/%s/" % (domain, post.slug)
    subject = "Your post in was approved!"
    message = render_to_string('approved_email.html', {
        'link': link,
        'title': post.title,
        'username': user.username
    })
    send_mail(subject, '', settings.EMAIL_HOST_USER, [user.email],
              fail_silently=False, html_message=message)
