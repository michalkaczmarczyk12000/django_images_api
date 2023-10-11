from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import UserCustom, Tier
from . forms import CustomUserCreationForm
# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = UserCustom
    list_display = [
        "username",
        "user_tier",
        "is_staff"
    ]
    list_display_links = ["username"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("user_tier",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("user_tier",)}),)


admin.site.register(UserCustom, CustomUserAdmin)
admin.site.register(Tier)
