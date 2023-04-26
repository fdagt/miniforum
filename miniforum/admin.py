from django.contrib import admin

from .models import Thread, Post

class PostInline(admin.StackedInline):
    model = Post
    extra = 1
    
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title']
    inlines = [PostInline]
    
admin.site.register(Thread, ThreadAdmin)
