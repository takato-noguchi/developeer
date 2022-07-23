from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import User, Profile, Course, Project, Comment, Plan

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ('username','email', 'img', 'selfIntro', 'github_url', 'password')}),
        (_('Personal Info'), {'fields': ()}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2')
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Plan)
