from django.db import models
from django.contrib.auth.models import User

class LottoTicket(models.Model):
    TICKET_TYPE_CHOICES = [
        ('AUTO', '자동'),
        ('MANUAL', '수동'),
    ]
    STATUS_CHOICES = [
        ('ACTIVE', '활성'),
        ('CHECKED', '확인완료'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    numbers = models.CharField(max_length=50)  # 콤마로 구분된 6개 숫자
    ticket_type = models.CharField(max_length=6, choices=TICKET_TYPE_CHOICES)
    purchase_date = models.DateTimeField(auto_now_add=True)
    draw_date = models.DateField()
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='ACTIVE')
    prize_rank = models.IntegerField(null=True, blank=True)  # 1-5등 또는 낙첨(0)
    prize_amount = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)

class DrawResult(models.Model):
    draw_number = models.IntegerField(unique=True)
    draw_date = models.DateField()
    winning_numbers = models.CharField(max_length=50)  # 콤마로 구분된 6개 숫자
    bonus_number = models.IntegerField()
    total_sales = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Statistics(models.Model):
    draw_result = models.OneToOneField(DrawResult, on_delete=models.CASCADE)
    total_tickets = models.IntegerField(default=0)
    auto_tickets = models.IntegerField(default=0)
    manual_tickets = models.IntegerField(default=0)
    first_prize_winners = models.IntegerField(default=0)
    second_prize_winners = models.IntegerField(default=0)
    third_prize_winners = models.IntegerField(default=0)
    fourth_prize_winners = models.IntegerField(default=0)
    fifth_prize_winners = models.IntegerField(default=0)
