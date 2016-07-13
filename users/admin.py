from django.contrib import admin
from users.models import User, Group 
from users.forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.models import Group as StandartGroup
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': (
            'first_name',
            'last_name',
            'email',
            'avatar',
            'personal_info',
            'favorite_posts',
            'key_expires'
        )}),
        ('Links', {'classes': ('collapse',), 'fields': ('website', 'facebook', 'gplus',
                              'twitter', 'github', 'linkedin', 'vk')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )


class GroupAdmin(admin.ModelAdmin):
    model = Group
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)

admin.site.unregister(StandartGroup)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)