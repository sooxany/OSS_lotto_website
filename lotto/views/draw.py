from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from datetime import datetime
import random
from ..models import DrawResult, Statistics
from .utils import check_winners  # 별도 유틸리티로 당첨 확인 분리

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def draw_numbers(request):
    if request.method == 'POST':
        # 당첨 번호 생성
        winning_numbers = random.sample(range(1, 46), 7)
        main_numbers = winning_numbers[:6]
        bonus_number = winning_numbers[6]

        # 마지막 추첨 회차 계산
        last_draw = DrawResult.objects.order_by('-draw_number').first()
        new_draw_number = (last_draw.draw_number + 1) if last_draw else 1

        # 추첨 결과 저장
        draw_result = DrawResult.objects.create(
            draw_number=new_draw_number,
            draw_date=datetime.now().date(),
            winning_numbers=','.join(map(str, main_numbers)),
            bonus_number=bonus_number
        )

        # Statistics 객체 생성은 utils.py의 check_winners에서 처리하도록 이 부분 제거

        # 당첨자 확인 및 통계 업데이트
        check_winners(draw_result)

        messages.success(request, f'{new_draw_number}회차 추첨이 완료되었습니다.')
        return redirect('statistics')
    return render(request, 'lotto/draw.html')