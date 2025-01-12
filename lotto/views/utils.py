# lotto/views/utils.py
from ..models import LottoTicket  # LottoTicket 모델을 임
from ..models import Statistics # LottoTicket 모델을 임

def check_winners(draw_result):
    winning_nums = set(map(int, draw_result.winning_numbers.split(',')))
    bonus_num = draw_result.bonus_number

    # 추첨일에 해당하는 티켓만 필터링
    tickets = LottoTicket.objects.filter(draw_date=draw_result.draw_date, status='ACTIVE')
    
    # 통계 객체 가져오기 또는 생성하기
    stats, created = Statistics.objects.get_or_create(draw_result=draw_result, 
        defaults={
            'total_tickets': 0,
            'auto_tickets': 0,
            'manual_tickets': 0,
            'first_prize_winners': 0,
            'second_prize_winners': 0,
            'third_prize_winners': 0,
            'fourth_prize_winners': 0,
            'fifth_prize_winners': 0
        }
    )

    # 통계 초기화 (매번 새로 계산)
    stats.auto_tickets = 0
    stats.manual_tickets = 0
    stats.first_prize_winners = 0
    stats.second_prize_winners = 0
    stats.third_prize_winners = 0
    stats.fourth_prize_winners = 0
    stats.fifth_prize_winners = 0

    for ticket in tickets:
        # 자동/수동 티켓 수 먼저 업데이트
        if ticket.ticket_type == 'AUTO':
            stats.auto_tickets += 1
        else:
            stats.manual_tickets += 1

        ticket_nums = set(map(int, ticket.numbers.split(',')))
        matched = len(winning_nums.intersection(ticket_nums))

        # 당첨 처리
        if matched == 6:
            ticket.prize_rank = 1
            ticket.prize_amount = 2000000000
            stats.first_prize_winners += 1
        elif matched == 5 and bonus_num in ticket_nums:
            ticket.prize_rank = 2
            ticket.prize_amount = 50000000
            stats.second_prize_winners += 1
        elif matched == 5:
            ticket.prize_rank = 3
            ticket.prize_amount = 1500000
            stats.third_prize_winners += 1
        elif matched == 4:
            ticket.prize_rank = 4
            ticket.prize_amount = 50000
            stats.fourth_prize_winners += 1
        elif matched == 3:
            ticket.prize_rank = 5
            ticket.prize_amount = 5000
            stats.fifth_prize_winners += 1
        else:
            ticket.prize_rank = 0
            ticket.prize_amount = 0

        ticket.status = 'CHECKED'
        ticket.save()

    stats.total_tickets = tickets.count()
    stats.save()

