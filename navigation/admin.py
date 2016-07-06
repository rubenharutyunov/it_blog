from django.contrib import admin
from django.db import models
from django.forms import widgets
from navigation.models import BlogNavigation, BlogNavigationItem
from navigation.forms import NavigationItemForm
from django.forms import BaseInlineFormSet


class CustomInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(CustomInlineFormSet, self).clean()
        for form in self.forms:
            print(form.instanse)


class BlogNavigationInline(admin.TabularInline):
    model = BlogNavigationItem
    form = NavigationItemForm
    verbose_name = "Menu Item"
    verbose_name_plural = "Menu Items"
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': widgets.TextInput(attrs={'size': 14})},
        models.URLField: {'widget': widgets.TextInput(attrs={'size': 14})},
    }

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(BlogNavigationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'parent':
            if request.obj is not None:
                field.queryset = field.queryset.filter(nav__exact=request.obj)
            else:
                field.queryset = field.queryset.none()
        return field


class BlogNavigationAdmin(admin.ModelAdmin):
    fields = ('name',)
    inlines = (BlogNavigationInline,)

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request.obj = obj
        return super(BlogNavigationAdmin, self).get_form(request, obj, **kwargs)


class BlogNavigationItemAdmin(admin.ModelAdmin):
    form = NavigationItemForm
    fieldsets = (
        (None, {
            'fields': ('menu_name', 'post', 'page', 'custom_url', 'icon', 'parent', 'order')
        }),
        ('Advanced', {
            'fields': ('urls_name',),
            'classes': ('collapse',)
        })
    )

admin.site.register(BlogNavigation, BlogNavigationAdmin)
# admin.site.register(BlogNavigationItem, BlogNavigationItemAdmin)
