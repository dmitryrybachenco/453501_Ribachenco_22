from django.utils import timezone
from datetime import datetime, date, timedelta
from calendar import monthcalendar
from apps.core.models import CompanyInfo


def site_context(request):
    """Контекстный процессор для передачи данных во все шаблоны"""

    company_info = CompanyInfo.objects.first()

    server_now = timezone.localtime(timezone.now())
    server_time = server_now.strftime('%d/%m/%Y %H:%M:%S')
    server_date = server_now.strftime('%d/%m/%Y')

    today = server_now.date()
    year = today.year
    month = today.month

    calendar_matrix = monthcalendar(year, month)

    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    month_names = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
        5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
        9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }
    month_name = month_names[month]

    return {
        'site_name': company_info.company_name if company_info else 'Косметологический центр',
        'current_year': server_now.year,
        'server_time': server_time,
        'server_date': server_date,
        'server_timezone': timezone.get_current_timezone_name(),
        'calendar_year': year,
        'calendar_month': month,
        'calendar_month_name': month_name,
        'calendar_weekdays': weekdays,
        'calendar_matrix': calendar_matrix,
        'today': today,
        'company_info': company_info,
    }