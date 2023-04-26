from django.contrib import admin

from .models import Thread, Post, Report

class PostInline(admin.StackedInline):
    model = Post
    extra = 1
    
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title']
    inlines = [PostInline]
    
admin.site.register(Thread, ThreadAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ['synopsis', 'created_at', 'dealt_at']
    list_filter = ['created_at', 'dealt_at']
    
admin.site.register(Report, ReportAdmin)
