from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.
# Passwords: testuser123


class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=50, default="testuser123")
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    profession = models.CharField(max_length=50, null=True, blank=True)
    profile_user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.first_name + " " + self.last_name


class BlockedProfile(models.Model):
    blocked_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="blocked_by", null=True, blank=True)
    users = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="blocked_users", null=True, blank=True)

    def __str__(self):
        return self.blocked_by.first_name + " " + self.users.first_name


class Post(models.Model):
    post_title = models.CharField(max_length=30)
    post_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, editable=False)
    post_content = models.TextField(max_length=200)
    post_creation_date = models.DateTimeField(default=datetime.now())
    post_last_edit = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_title


class PostComment(models.Model):
    comment_content = models.TextField(max_length=200)
    comment_timestamp = models.DateTimeField(auto_now_add=True)
    comment_user = models.ForeignKey(Profile, on_delete=models.CASCADE, editable=False)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_content + " " + self.comment_timestamp.__str__()




