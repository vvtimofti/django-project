from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=20)
    profile_picture = models.ImageField(
        default="default.png", 
        upload_to="profile_pics", 
        null=True, 
        blank=True
    )
    bio = models.TextField(max_length=300, blank=True, null=True)
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="followers"
    )

    def __str__(self) -> str:
        return f"{self.user.username} Profile"

    def get_absolute_url(self):
        return reverse("profile", kwargs={"username": self.user.username})

    def get_follower_count(self):
        return self.followers.count()

    def get_following_count(self):
        return self.following.count()
