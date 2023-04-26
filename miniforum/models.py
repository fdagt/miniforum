from django.db import models
from django.contrib.auth.models import User

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
        return self.created_at.strftime("%Y/%m/%d") + " (" + ["月", "火", "水", "木", "金", "土", "日"][self.created_at.weekday()] + ") "+ self.created_at.strftime("%H:%M")
