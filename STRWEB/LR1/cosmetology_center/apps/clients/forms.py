from django import forms
from .models import Appointment
from apps.services.models import Service
from apps.doctors.models import Doctor, Schedule
from datetime import date, time, datetime
from django.core.exceptions import ValidationError


class AppointmentForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Услуга'
    )
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Врач',
        required=False
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Дата приема'
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label='Время приема'
    )

    class Meta:
        model = Appointment
        fields = ['service', 'doctor', 'date', 'time']

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        doctor = cleaned_data.get('doctor')
        appointment_date = cleaned_data.get('date')
        appointment_time = cleaned_data.get('time')

        if appointment_date and appointment_date < date.today():
            raise ValidationError('Нельзя записаться на прошедшую дату')

        if doctor and service:
            if not doctor.services.filter(id=service.id).exists():
                raise ValidationError(
                    f'Доктор {doctor.user.get_full_name()} не предоставляет услугу "{service.name}". '
                    f'Пожалуйста, выберите другого врача или другую услугу.'
                )

        if doctor and appointment_date and appointment_time:
            existing = Appointment.objects.filter(
                doctor=doctor,
                date=appointment_date,
                time=appointment_time,
                status='scheduled'
            ).exists()

            if existing:
                raise ValidationError('Это время уже занято')

            schedule = Schedule.objects.filter(
                doctor=doctor,
                date=appointment_date,
                start_time__lte=appointment_time,
                end_time__gte=appointment_time,
                is_available=True
            ).exists()

            if not schedule:
                raise ValidationError('Врач не работает в выбранное время')

        return cleaned_data