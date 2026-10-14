from django.db import models
from apps.users.models import User
from apps.services.models import Service


class DoctorSpecialization(models.Model):
    name = models.CharField('Специализация', max_length=100)
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специализация врача'
        verbose_name_plural = 'Специализации врачей'


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specializations = models.ManyToManyField(DoctorSpecialization, related_name='doctors')
    services = models.ManyToManyField(Service, related_name='doctors')
    experience_years = models.IntegerField('Опыт работы (лет)', default=0)
    education = models.TextField('Образование')
    photo = models.ImageField('Фото', upload_to='doctors/', blank=True, null=True)

    def __str__(self):
        return f"Др. {self.user.get_full_name()}"

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField('Дата')
    start_time = models.TimeField('Время начала')
    end_time = models.TimeField('Время окончания')
    is_available = models.BooleanField('Доступно', default=True)

    def __str__(self):
        return f"{self.doctor} - {self.date} {self.start_time}-{self.end_time}"

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        unique_together = ['doctor', 'date', 'start_time']