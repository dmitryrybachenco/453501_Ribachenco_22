from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Doctor, DoctorSpecialization, Schedule
from apps.services.models import Service
from datetime import date, timedelta


def doctor_list(request):
    """Список всех врачей"""
    doctors = Doctor.objects.all().select_related('user')

    specialization_id = request.GET.get('specialization')
    if specialization_id:
        doctors = doctors.filter(specializations__id=specialization_id)

    query = request.GET.get('q')
    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )

    specializations = DoctorSpecialization.objects.annotate(
        doctor_count=Count('doctors')
    ).filter(doctor_count__gt=0)

    context = {
        'doctors': doctors,
        'specializations': specializations,
        'selected_specialization': specialization_id,
        'query': query,
    }
    return render(request, 'doctors/doctor_list.html', context)


def doctor_detail(request, pk):
    """Детальная страница врача"""
    doctor = get_object_or_404(Doctor, pk=pk)

    services = doctor.services.filter(is_active=True)

    today = date.today()
    end_date = today + timedelta(days=14)

    available_slots = Schedule.objects.filter(
        doctor=doctor,
        date__gte=today,
        date__lte=end_date,
        is_available=True
    ).order_by('date', 'start_time')[:10]

    context = {
        'doctor': doctor,
        'services': services,
        'available_slots': available_slots,
    }
    return render(request, 'doctors/doctor_detail.html', context)


def doctor_schedule(request, pk):
    """Расписание врача на неделю"""
    doctor = get_object_or_404(Doctor, pk=pk)

    week_start = request.GET.get('week_start')
    if week_start:
        week_start = date.fromisoformat(week_start)
    else:
        week_start = date.today()

    week_days = []
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        schedules = Schedule.objects.filter(
            doctor=doctor,
            date=current_date
        ).order_by('start_time')
        week_days.append({
            'date': current_date,
            'schedules': schedules
        })

    context = {
        'doctor': doctor,
        'week_days': week_days,
        'prev_week': week_start - timedelta(days=7),
        'next_week': week_start + timedelta(days=7),
    }
    return render(request, 'doctors/doctor_schedule.html', context)