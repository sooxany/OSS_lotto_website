from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from ..models import Statistics

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def statistics(request):
    stats = Statistics.objects.select_related('draw_result').order_by('-draw_result__draw_date')
    return render(request, 'lotto/statistics.html', {'stats': stats})
