from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Thread(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)
    
class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=100)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)
    content = models.CharField(max_length=1000)
    
    def format_created_at(self):
        localtime = timezone.localtime(self.created_at)
        date = localtime.strftime("%Y/%m/%d")
        dayOfWeek = ["月", "火", "水", "木", "金", "土", "日"][localtime.weekday()]
        time = localtime.strftime("%H:%M")
        return date + " (" + dayOfWeek + ") " + time

class Report(models.Model):
    thread = models.ForeignKey(Thread, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=100)
    dealt_at = models.DateTimeField(default=None, null=True, blank=True)
    content = models.CharField(max_length=1000)

    def synopsis(self):
        return self.content[0:20]
