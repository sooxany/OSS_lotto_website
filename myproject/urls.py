from django.contrib import admin
from django.urls import path, include  # path 임포트 확인
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # 로그인 페이지 URL 설정
    path('', include('lotto.urls')),  # 기본 경로로 lotto 앱 URL 연결
]
