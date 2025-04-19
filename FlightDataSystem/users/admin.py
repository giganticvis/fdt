from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Division, Flight

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'division')
    list_filter = ('role', 'division')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'role', 'division')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'division'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Division)
admin.site.register(Flight)
