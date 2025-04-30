from django.contrib import admin
from battle.models import Battle, BattleParticipant

@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'start_time', 'end_time', 'status', 'battle_type', 'prize_pool')
    list_filter = ('status', 'battle_type', 'created_at')
    search_fields = ('title', 'description', 'creator__username')
    readonly_fields = ('created_at',)
    filter_horizontal = ('participants',)

@admin.register(BattleParticipant)
class BattleParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'battle', 'score', 'submission_time', 'status')
    list_filter = ('status', 'submission_time')
    search_fields = ('user__username', 'battle__title')
    readonly_fields = ('submission_time',)
