from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import uuid

from django.urls import reverse

MAX_CONTENT_LENGTH = 350
User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    post_key = models.UUIDField(
        default=uuid.uuid4, max_length=40, unique=True, editable=False)
    parent_post = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    post_content = models.TextField(
        max_length=MAX_CONTENT_LENGTH, blank=False, null=False)
    datetime = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='post-media', blank=True, null=True)
    views_count = models.IntegerField(default=0)
    reposted_by = models.ManyToManyField(User, blank=True, through="Repost", related_name="reposts")
    likes = models.ManyToManyField(User, blank=True, through="Like", related_name='post_likes')
    bookmarks = models.ManyToManyField(User, blank=True, through="Bookmark", related_name='post_bookmarks')
    modified = models.BooleanField(default=False)
    is_reply = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)

    def __str__(self):
        parent_post_info = f"{self.parent_post.user.username} on {self.parent_post.post_key}" if self.parent_post else self.post_key
        return f"{self.user.username}-{parent_post_info}"
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"username": self.user.username, "post_key": self.post_key})
    
    def clean(self):
        if len(self.post_content) > MAX_CONTENT_LENGTH:
            raise ValidationError(
                f"Post content cannot exceed {MAX_CONTENT_LENGTH} characters.")
        if self.is_video and not self.media:
            raise ValidationError(f"Video posts must have a media uploaded.")
        
    class Meta:
        ordering = ['-datetime']
        

class Repost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="u_reposts")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="p_reposts")
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reposted: {self.post} by {self.user.username}"
    
    class Meta:
        ordering = ['-datetime']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="u_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="p_likes")
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Liked: {self.post} by {self.user.username}"
    
    class Meta:
        ordering = ['-datetime']


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="u_bookmarks")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="p_bookmarks")
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Bookmarked: {self.post} by {self.user.username}"
    
    class Meta:
        ordering = ['-datetime']


class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    post_creator = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
