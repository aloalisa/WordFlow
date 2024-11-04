from datetime import timezone

from django.contrib.auth.models import User
# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    section = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')


    def __str__(self):
        return self.title


class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"




