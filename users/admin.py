from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


User = get_user_model()


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональные данные', 
            {'fields': ('first_name', 'last_name', 'email')}
        ),
        ('Разрешения', {'fields': ('is_staff', 'is_active')}),
    )
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    ordering = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(User, MyUserAdmin)