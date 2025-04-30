from django.contrib import admin
from transactions.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'amount', 'transaction_type', 'status', 'created_at')
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = ('transaction_id', 'user__username', 'related_battle__title')
    readonly_fields = ('created_at', 'transaction_id')
    ordering = ('-created_at',)
