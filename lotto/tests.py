from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import LottoTicket, DrawResult, Statistics
from datetime import datetime, timedelta

class LottoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        
    def test_purchase_auto_ticket(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('purchase_ticket'), {
            'ticket_type': 'AUTO'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LottoTicket.objects.count(), 1)
        ticket = LottoTicket.objects.first()
        self.assertEqual(ticket.ticket_type, 'AUTO')
        self.assertEqual(len(ticket.numbers.split(',')), 6)
        
    def test_purchase_manual_ticket(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('purchase_ticket'), {
            'ticket_type': 'MANUAL',
            'number_0': '1',
            'number_1': '2',
            'number_2': '3',
            'number_3': '4',
            'number_4': '5',
            'number_5': '6'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LottoTicket.objects.count(), 1)
        ticket = LottoTicket.objects.first()
        self.assertEqual(ticket.ticket_type, 'MANUAL')
        self.assertEqual(ticket.numbers, '1,2,3,4,5,6')
        
    def test_draw_numbers_admin_only(self):
        # 일반 사용자 접근 시도
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('draw_numbers'))
        self.assertEqual(response.status_code, 302)  # 리다이렉트 (접근 거부)
        
        # 관리자 접근
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('draw_numbers'))
        self.assertEqual(response.status_code, 200)
        
    def test_winning_check(self):
        self.client.login(username='admin', password='admin123')
        # 테스트용 티켓 생성
        ticket = LottoTicket.objects.create(
            user=self.user,
            numbers='1,2,3,4,5,6',
            ticket_type='MANUAL',
            draw_date=datetime.now().date(),
            status='ACTIVE'
        )
        
        # 당첨 번호 추첨 (1등 당첨되도록 설정)
        draw_result = DrawResult.objects.create(
            draw_number=1,
            draw_date=datetime.now().date(),
            winning_numbers='1,2,3,4,5,6',
            bonus_number=7
        )
        
        from .views import check_winners
        check_winners(draw_result)
        
        # 티켓 상태 확인
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, 'CHECKED')
        self.assertEqual(ticket.prize_rank, 1)
        
        # 통계 확인
        stats = Statistics.objects.first()
        self.assertEqual(stats.first_prize_winners, 1)