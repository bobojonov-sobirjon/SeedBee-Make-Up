from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models
from apps.accounts.managers.custom_user import CustomUserManager
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_("Email"), null=True, blank=True)
    username = models.CharField(max_length=250, unique=True, verbose_name=_("Username"), null=True, blank=True)
    first_name = models.CharField(max_length=30, verbose_name=_("First Name"), null=True, blank=True)
    last_name = models.CharField(max_length=30, verbose_name=_("Last Name"), null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_("Avatar"))
    is_agree = models.BooleanField(null=True, blank=True, default=False, verbose_name=_("Agreement to Terms"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Staff"))

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True, verbose_name=_("Groups"))

    user_permissions = models.ManyToManyField(Permission, related_name="customuser_set", blank=True,
                                              verbose_name=_("User Permissions"))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        first_name = self.first_name or ""
        last_name = self.last_name or ""
        username = self.username or ""
        email = self.email or ""

        if first_name or last_name:
            return f"{first_name} {last_name}".strip()
        elif username:
            return username
        elif email:
            return email
        else:
            return f"User {self.pk}"
