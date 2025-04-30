from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Permission
from user.models import *


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = UserChangeForm.Meta.fields


class UserAdminView(UserAdmin):
    form = CustomUserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'level', 'wallet_balance', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'avatar', 'bio', 'level', 'experience_points', 'wallet_balance')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_battles_won', 'total_battles_participated', 'ranking_points')
    search_fields = ('user__username',)


admin.site.register(Permission)
admin.site.register(User, UserAdminView)

