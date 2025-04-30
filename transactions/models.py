from django.db import models
from user.models import User
from battle.models import Battle

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20)  # Deposit/Withdrawal/Prize/Entry Fee
    status = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100, unique=True)
    related_battle = models.ForeignKey(Battle, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payment"
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.user.username}"
