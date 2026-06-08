# apps/analytics/views.py
import logging
import io
import base64
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta

from apps.analytics.models import Review
from apps.clients.models import Appointment, Payment
from apps.services.models import Service
from apps.users.models import User
from apps.doctors.models import Doctor

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Comic Neue']
plt.rcParams['axes.unicode_minus'] = False

logger = logging.getLogger(__name__)


def create_daily_appointments_chart(daily_data):
    """Создает график количества приемов по дням недели"""
    dates = [item['date'] for item in daily_data]
    counts = [item['count'] for item in daily_data]
    day_names = [item['day_name'] for item in daily_data]

    fig, ax = plt.subplots(figsize=(10, 5))

    bars = ax.bar(range(len(dates)), counts, color='#3498db', width=0.6)

    ax.set_xlabel('День недели', fontsize=12)
    ax.set_ylabel('Количество приемов', fontsize=12)
    ax.set_title('Количество приемов по дням (за последние 7 дней)', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels([f'{day_names[i]}\n{dates[i]}' for i in range(len(dates))], fontsize=10)

    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.annotate(f'{count}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold')


    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    if counts:
        ax.set_ylim(0, max(counts) + max(counts) * 0.2)

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return image_base64


def create_hourly_appointments_chart(hourly_data):
    """Создает график количества приемов по часам"""
    hours = [item['hour'] for item in hourly_data]
    counts = [item['count'] for item in hourly_data]

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(hours, counts, marker='o', linewidth=2, markersize=8, color='#2ecc71')
    ax.fill_between(range(len(hours)), counts, alpha=0.3, color='#2ecc71')

    ax.set_xlabel('Время (часы)', fontsize=12)
    ax.set_ylabel('Количество приемов', fontsize=12)
    ax.set_title('Количество приемов по часам (за последние 7 дней)', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(hours)))
    ax.set_xticklabels(hours, rotation=45, fontsize=10)

    for hour, count in zip(range(len(hours)), counts):
        ax.annotate(f'{count}',
                    xy=(hour, count),
                    xytext=(5, 5),
                    textcoords="offset points",
                    fontsize=9,
                    fontweight='bold')

    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    if counts:
        ax.set_ylim(0, max(counts) + max(counts) * 0.3)

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return image_base64


def create_age_distribution_chart(age_groups):
    """Создает круговую диаграмму возрастного распределения"""
    labels = ['18-25 лет', '26-35 лет', '36-50 лет', '50+ лет']
    sizes = [age_groups['18_25'], age_groups['26_35'], age_groups['36_50'], age_groups['50_plus']]
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']

    data = [(l, s, c) for l, s, c in zip(labels, sizes, colors) if s > 0]
    if not data:
        return None

    labels, sizes, colors = zip(*data)

    fig, ax = plt.subplots(figsize=(8, 6))

    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                      autopct='%1.1f%%', startangle=90,
                                      textprops={'fontsize': 10})

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    ax.set_title('Возрастное распределение клиентов', fontsize=14, fontweight='bold')
    ax.axis('equal')

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return image_base64


def create_top_doctors_chart(doctor_stats):
    """Создает горизонтальный бар-чарт топ врачей"""
    if not doctor_stats:
        return None

    names = [doc.user.get_full_name() for doc in doctor_stats]
    counts = [doc.appointments_count for doc in doctor_stats]

    fig, ax = plt.subplots(figsize=(10, 5))

    y_pos = range(len(names))
    bars = ax.barh(y_pos, counts, color='#9b59b6')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel('Количество приемов', fontsize=12)
    ax.set_title('Топ-5 врачей по количеству приемов', fontsize=14, fontweight='bold')
    ax.invert_yaxis()

    for bar, count in zip(bars, counts):
        ax.annotate(f'{count}',
                    xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0),
                    textcoords="offset points",
                    ha='left', va='center',
                    fontsize=10)

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return image_base64


@staff_member_required
def statistics(request):
    """Статистические показатели с графиками"""
    user_tz = request.session.get('timezone', 'Europe/Minsk')

    total_clients = User.objects.filter(role='client').count()
    total_doctors = Doctor.objects.count()
    total_services = Service.objects.filter(is_active=True).count()
    total_appointments = Appointment.objects.count()

    service_stats = Service.objects.annotate(
        appointment_count=Count('appointments')
    ).order_by('-appointment_count')

    most_popular_service = service_stats.first()

    revenue_by_service = Service.objects.annotate(
        total_revenue=Sum('appointments__payment__amount', filter=Q(appointments__payment__is_paid=True))
    ).order_by('-total_revenue')

    today = timezone.now().date()
    week_ago = today - timedelta(days=6)

    appointments_by_date = {}
    for i in range(7):
        current_date = week_ago + timedelta(days=i)
        appointments_by_date[current_date] = 0

    appointments = Appointment.objects.filter(
        date__gte=week_ago,
        date__lte=today
    ).values('date').annotate(count=Count('id'))

    for app in appointments:
        appointments_by_date[app['date']] = app['count']

    daily_data = []
    for date_obj, count in appointments_by_date.items():
        daily_data.append({
            'date': date_obj.strftime('%d/%m'),
            'day_name': get_day_name_ru(date_obj.weekday()),
            'count': count
        })


    appointments_by_hour = {hour: 0 for hour in range(9, 21)}
    week_appointments = Appointment.objects.filter(
        date__gte=week_ago,
        date__lte=today
    )
    for appointment in week_appointments:
        hour = appointment.time.hour
        if hour in appointments_by_hour:
            appointments_by_hour[hour] += 1

    hourly_data = []
    for hour, count in appointments_by_hour.items():
        hourly_data.append({'hour': f"{hour}:00", 'count': count})

    age_groups = {'18_25': 0, '26_35': 0, '36_50': 0, '50_plus': 0}
    for client in User.objects.filter(role='client'):
        age = client.get_age()
        if 18 <= age <= 25:
            age_groups['18_25'] += 1
        elif 26 <= age <= 35:
            age_groups['26_35'] += 1
        elif 36 <= age <= 50:
            age_groups['36_50'] += 1
        elif age > 50:
            age_groups['50_plus'] += 1

    doctor_stats = Doctor.objects.annotate(
        appointments_count=Count('appointments'),
        total_revenue=Sum('appointments__payment__amount', filter=Q(appointments__payment__is_paid=True))
    ).order_by('-appointments_count')[:5]

    avg_rating = Review.objects.filter(is_moderated=True).aggregate(Avg('rating'))['rating__avg'] or 0

    daily_chart = create_daily_appointments_chart(daily_data)
    hourly_chart = create_hourly_appointments_chart(hourly_data)
    age_chart = create_age_distribution_chart(age_groups)
    doctors_chart = create_top_doctors_chart(doctor_stats)

    context = {
        'total_clients': total_clients,
        'total_doctors': total_doctors,
        'total_services': total_services,
        'total_appointments': total_appointments,
        'most_popular_service': most_popular_service,
        'revenue_by_service': revenue_by_service[:5],
        'daily_chart': daily_chart,
        'hourly_chart': hourly_chart,
        'age_chart': age_chart,
        'doctors_chart': doctors_chart,
        'doctor_stats': doctor_stats,
        'avg_rating': round(avg_rating, 1),
        'user_timezone': user_tz,
    }

    return render(request, 'analytics/statistics.html', context)


def get_day_name_ru(weekday):
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    return days[weekday]