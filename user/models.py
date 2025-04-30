from datetime import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Extends Django's built-in User model
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    level = models.IntegerField(default=1)
    experience_points = models.IntegerField(default=0)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    social_links = models.JSONField(default=dict)  # Store social media links
    achievements = models.ManyToManyField('Achievement')
    total_battles_won = models.IntegerField(default=0)
    total_battles_participated = models.IntegerField(default=0)
    ranking_points = models.IntegerField(default=0)

    class Meta:
        db_table = "profile"
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='achievements/')
    points = models.IntegerField()
    requirements = models.JSONField()  # Store achievement criteria

    class Meta:
        db_table = "achievement"
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'

    def __str__(self):
        return self.name