from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser


class MyUserAdmin(UserAdmin):
    # search_fields = ['area_id', 'area_name']
    list_display = ['username']
    # exclude = ['first_name', 'last_name', 'email', 'date_joined']


class MyUserAdmins(UserAdmin):
    model = AppUser

    fieldsetss = UserAdmin.fieldsets + (
        (None, {'fields': ('reg_person',)}),
    )
    fieldsets = (
        (None, {'fields': (
            'username', 'password', 'reg_person', 'is_active', 'is_staff',
            'password_changed_timestamp')}),)

admin.site.register(AppUser, MyUserAdmins)

# admin.site.register(AppUser, MyUserAdmin)
