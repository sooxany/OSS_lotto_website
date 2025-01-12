# 내 티켓 보기 관련

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import LottoTicket

@login_required
def my_tickets(request):
    tickets = LottoTicket.objects.filter(user=request.user).order_by('-purchase_date')
    return render(request, 'lotto/my_tickets.html', {'tickets': tickets})
