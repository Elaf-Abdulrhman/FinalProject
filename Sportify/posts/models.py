from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    photo = models.ImageField(upload_to='posts/photos/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"

class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"

