from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import ugettext as _
import bleach


def send_approved_email(post):
    user = post.author
    domain = Site.objects.get_current().domain
    link = "http://%s/post/%s/" % (domain, post.slug)
    subject = _("Your post in was approved!")
    message = render_to_string('approved_email.html', {
        'link': link,
        'title': post.title,
        'username': user.username
    })
    send_mail(subject, '', settings.EMAIL_HOST_USER, [user.email],
              fail_silently=False, html_message=message)


allowed_attrs = {
    '*': ['class', 'style'],
    'a': ['href', 'rel', 'id', 'name'],
    'img': ['src', 'alt', 'title'],
    'p': ['dir'],
    'table': ['border', 'cellpadding', 'cellspacing', 'align', 'summary'],
    'th': ['scope']
}

allowed_tags = [
    'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'p', 'strong', 'em', 'u', 's', 'br',
    'sub', 'sup', 'ol', 'ul', 'li', 'table', 'tbody', 'tr', 'td', 'hr', 'pre', 'code'
]

allowed_styles = [
    'margin', 'margin-left', 'margin-right', 'margin-top', 'margin-bottom', 'padding', 'padding-left',
    'padding-right', 'padding-top', 'padding-bottom', 'text-align', 'page-break-after'
]


def clean_untrusted_tags(text):
    return bleach.clean(text, tags=allowed_tags, attributes=allowed_attrs, styles=allowed_styles)