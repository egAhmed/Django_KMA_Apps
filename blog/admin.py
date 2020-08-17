from django.contrib import admin
from .models import Blog

# admin.site.register(Blog) # 
# Register your models here.

@admin.register(Blog) # Make a filter column in admin site
class Blogadmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    list_filter = ('title', 'pub_date', 'body')
