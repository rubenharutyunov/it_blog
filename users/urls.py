from django.conf.urls import url, include
from users.views import sign_in, sign_out, get_users, get_user_posts, get_user_comments, get_user, sign_up,\
    activate_account, new_activation_link
from django.contrib.auth.views import password_reset, password_change_done, password_change, password_reset_complete, password_reset_confirm, password_reset_done

urlpatterns = [
    url(r'^users/', get_users, name='users'),
    url(r'^user/(?P<username>[\w-]+)/$', get_user, name='user'),
    url(r'^profile/$', get_user, name='profile'),
    url(r'^user/(?P<username>[\w-]+)/posts/', get_user_posts, name='user_posts'),
    url(r'^user/(?P<username>[\w-]+)/comments/', get_user_comments, name='user_comments'),
    url(r'^sign_in/', sign_in, name='sign_in'),
    url(r'^sign_out/', sign_out, name='sign_out'),
    url(r'^sign_up/', sign_up, name='sign_up'),
    url(r'^edit_profile/', sign_up, {'edit': True}, name='edit_profile'),
    url(r'^activate/(?P<activation_key>[\w-]+)/$', activate_account, name='activate'),
    url(r'^new_activation_link/(?P<username>[\w-]+)/$', new_activation_link, name='new_activation_link'),
    url(r'^reset_password/$', password_reset, {
        'template_name': 'reset_password.html',
        'email_template_name': 'password_reset_email.html',
        'html_email_template_name': 'password_reset_email.html',
        'subject_template_name': 'password_reset_subject.txt'
    }, name="reset_password"),
    url(r'^reset_password/done/$', password_reset_done, {
        'template_name': 'password_reset_done.html'
    }, name='password_reset_done'),
    url(r'^reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm,
     {'post_reset_redirect': '/',
        'template_name': 'password_reset_confirm.html'
     }, name='password_reset_confirm'),
]