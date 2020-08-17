from django.contrib import admin
from .models import UserProfileInfo

admin.site.register(UserProfileInfo)
# Register your models here.

# @admin.register(UserProfileInfo)# Make a filter column in admin site
# class UserProfileInfoadmin(admin.ModelAdmin):
#     list_display = ('user',)
#     list_filter = ('user',)
