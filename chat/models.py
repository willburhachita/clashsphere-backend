from django.db import models
from user.models import User
from battle.models import Battle

# Create your models here.

class ChatRoom(models.Model):
    battle = models.OneToOneField(Battle, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_room"
        verbose_name = 'Chat Room'
        verbose_name_plural = 'Chat Rooms'

    def __str__(self):
        return f"Chat for {self.battle.title}"

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_message"
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
