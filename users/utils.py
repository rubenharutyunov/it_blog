import hashlib
import random
import datetime
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.conf import settings


TOMORROW = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=1),
                                      "%Y-%m-%d %H:%M:%S")


def generate_activation_key(username):
    salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
    if isinstance(username, str):
        username = username.encode('utf8')
    return hashlib.sha1(salt.encode('utf-8') + username).hexdigest()


def send_activation_email(username, activation_key, email):
    domain = Site.objects.get_current().domain
    link = "http://%s/activate/" % domain + activation_key
    subject = "IT Blog account activation"
    message = render_to_string('activation_email.html', {
        'activation_link': link,
        'username': username
    })
    send_mail(subject, '', settings.EMAIL_HOST_USER, [email],
              fail_silently=False, html_message=message)
