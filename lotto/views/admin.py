# views/admin.py
from django.contrib.auth.models import User
from django.http import HttpResponse

def assign_admin(request):
    try:
        user = User.objects.get(username='soojin')  # 'soojin' 사용자 찾기
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return HttpResponse('관리자 권한이 부여되었습니다.')
    except User.DoesNotExist:
        return HttpResponse('사용자가 존재하지 않습니다.')
