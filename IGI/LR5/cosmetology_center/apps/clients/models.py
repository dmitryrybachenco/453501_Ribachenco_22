from django.db import models
from apps.users.models import User
from apps.services.models import Service
from apps.doctors.models import Doctor


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Запланирован'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField('Дата приема')
    time = models.TimeField('Время приема')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)
    notes = models.TextField('Заметки', blank=True)

    def __str__(self):
        return f"Прием {self.client.get_full_name()} - {self.doctor} - {self.date}"

    class Meta:
        verbose_name = 'Прием'
        verbose_name_plural = 'Приемы'
        ordering = ['-date', '-time']


class Payment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField('Дата оплаты', auto_now_add=True)
    is_paid = models.BooleanField('Оплачено', default=False)

    def __str__(self):
        return f"Оплата {self.amount} руб. - {self.appointment}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'