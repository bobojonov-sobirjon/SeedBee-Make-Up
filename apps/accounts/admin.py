from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site

from apps.accounts.models import (
    CustomUser
)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'password', 'avatar')}),
        (_('Personal Information'),
         {'fields': ('first_name', 'last_name', 'email', 'is_agree')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Groups and Permissions'), {'fields': ('groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'avatar',
                'is_agree', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            ),
        }),
    )

    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(CustomUser, CustomUserAdmin)

# Customize admin site

admin.site.site_header = _("Seedbee.uz Администрирование")
admin.site.site_title = _("Seedbee.uz Администрирование")
admin.site.index_title = _("Добро пожаловать в панель администратора Seedbee.uz")

# Customize the admin interface for CustomUser
admin.site.unregister(Group)  # Unregister Group model as it's not needed


# Unregister Sites model as it's not needed
admin.site.unregister(Site)
