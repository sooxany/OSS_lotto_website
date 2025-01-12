# 로또 구매 관련

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
import random
from ..models import LottoTicket

@login_required
def purchase_ticket(request):
    if request.method == 'POST':
        ticket_type = request.POST.get('ticket_type')
        numbers = []

        if ticket_type == 'AUTO':
            numbers = random.sample(range(1, 46), 6)
            numbers.sort()
        else:  # MANUAL
            for i in range(6):
                num = int(request.POST.get(f'number_{i}'))
                if num < 1 or num > 45:
                    messages.error(request, '1부터 45 사이의 숫자를 선택해주세요.')
                    return redirect('purchase_ticket')
                numbers.append(num)
            numbers.sort()

        # 현재 진행 중인 회차의 추첨일 가져오기
        from ..models import DrawResult
        current_draw = DrawResult.objects.order_by('-draw_number').first()
        if not current_draw:
            # 아직 추첨 결과가 없는 경우 기본값 설정
            today = datetime.now().date()
            days_ahead = 5 - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            next_draw = today + timedelta(days=days_ahead)
        else:
            next_draw = current_draw.draw_date

        LottoTicket.objects.create(
            user=request.user,
            numbers=','.join(map(str, numbers)),
            ticket_type=ticket_type,
            draw_date=next_draw
        )

        messages.success(request, '로또 구매가 완료되었습니다.')
        return redirect('my_tickets')

    return render(request, 'lotto/purchase.html')