from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'image', 'view_count', 'date_created', 'is_published',)
    list_filter = ('date_created',)
    search_fields = ('title', 'content')
