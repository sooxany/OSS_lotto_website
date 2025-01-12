from django.contrib import admin
from .models import LottoTicket, DrawResult, Statistics

@admin.register(LottoTicket)
class LottoTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticket_type', 'numbers', 'purchase_date', 'draw_date', 'status', 'prize_rank')
    list_filter = ('ticket_type', 'status', 'draw_date')
    search_fields = ('user__username', 'numbers')

@admin.register(DrawResult)
class DrawResultAdmin(admin.ModelAdmin):
    list_display = ('draw_number', 'draw_date', 'winning_numbers', 'bonus_number')
    search_fields = ('draw_number', 'winning_numbers')

@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('draw_result', 'total_tickets', 'auto_tickets', 'manual_tickets',
                   'first_prize_winners', 'second_prize_winners')
    