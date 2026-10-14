from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Appointment, Payment
from .forms import AppointmentForm
from apps.services.models import Service
from apps.doctors.models import Doctor, Schedule


@login_required
def appointment_list(request):
    """Список записей текущего пользователя"""
    appointments = Appointment.objects.filter(
        client=request.user
    ).select_related('doctor', 'service', 'payment').order_by('-date', '-time')

    upcoming = appointments.filter(date__gte=timezone.now().date(), status='scheduled')
    past = appointments.filter(date__lt=timezone.now().date()) | appointments.exclude(status='scheduled')

    context = {
        'upcoming_appointments': upcoming,
        'past_appointments': past,
    }
    return render(request, 'clients/appointment_list.html', context)


@login_required
def create_appointment(request):
    """Создание новой записи на прием"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.save()

            Payment.objects.create(
                appointment=appointment,
                amount=appointment.service.price,
                is_paid=False
            )

            messages.success(request,
                             f'Вы успешно записаны на {appointment.service.name} {appointment.date} в {appointment.time}')
            return redirect('clients:appointment_list')
    else:
        initial = {}
        doctor_id = request.GET.get('doctor')
        service_id = request.GET.get('service')
        if doctor_id:
            initial['doctor'] = doctor_id
        if service_id:
            initial['service'] = service_id
        form = AppointmentForm(initial=initial)

    context = {
        'form': form,
    }
    return render(request, 'clients/create_appointment.html', context)


@login_required
def cancel_appointment(request, pk):
    """Отмена записи на прием"""
    appointment = get_object_or_404(Appointment, pk=pk, client=request.user)

    if appointment.status == 'scheduled' and appointment.date >= timezone.now().date():
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, f'Запись на {appointment.date} в {appointment.time} отменена')
    else:
        messages.error(request, 'Невозможно отменить эту запись')

    return redirect('clients:appointment_list')