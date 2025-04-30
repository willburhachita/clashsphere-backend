from django.db import models
from user.models import User

# Create your models here.

class Battle(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_battles')
    participants = models.ManyToManyField(User, through='BattleParticipant')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    prize_pool = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('UPCOMING', 'Upcoming'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled')
    ])
    battle_type = models.CharField(max_length=20)  # Public/Private
    max_participants = models.IntegerField()
    rules = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "battle"
        verbose_name = 'Battle'
        verbose_name_plural = 'Battles'

    def __str__(self):
        return self.title

class BattleParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)
    submission = models.FileField(upload_to='battle_submissions/', null=True)
    score = models.IntegerField(null=True)
    submission_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=20)  # Registered/Submitted/Evaluated

    class Meta:
        db_table = "battle_participant"
        verbose_name = 'Battle Participant'
        verbose_name_plural = 'Battle Participants'

    def __str__(self):
        return f"{self.user.username} - {self.battle.title}"
