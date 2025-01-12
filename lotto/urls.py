# lotto/urls.py
from django.urls import path  # path 임포트 확인
from .views.purchase import purchase_ticket # 로또 구매
from .views.draw import draw_numbers # 번호 추첨
from .views.statistics import statistics # 통계 보기
from .views.tickets import my_tickets # 내 티켓 보기
from .views.utils import check_winners # 번호 추첨
from .views.home import home  # 홈 화면
from .views.admin import assign_admin

urlpatterns = [
    path('', home, name='home'),  # 기본 경로
    path('purchase/', purchase_ticket, name='purchase_ticket'),
    path('my-tickets/', my_tickets, name='my_tickets'),
    path('draw/', draw_numbers, name='draw_numbers'),
    path('statistics/', statistics, name='statistics'),
    path('utils/', check_winners, name='check_winners'),
    path('assign-admin/', assign_admin, name='assign_admin')
]
