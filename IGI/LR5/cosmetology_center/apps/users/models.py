from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator
from datetime import date


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('doctor', 'Врач'),
        ('client', 'Клиент'),
    ]

    role = models.CharField('Роль', max_length=10, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(
        'Телефон',
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+375\s\(29\)\s\d{3}-\d{2}-\d{2}$',
                message='Формат: +375 (29) XXX-XX-XX'
            )
        ]
    )
    birth_date = models.DateField('Дата рождения')
    address = models.CharField('Адрес', max_length=255, blank=True)

    def get_age(self):
        if not self.birth_date:
            return 0
        today = date.today()
        age = today.year - self.birth_date.year
        if today.month < self.birth_date.month or \
                (today.month == self.birth_date.month and today.day < self.birth_date.day):
            age -= 1
        return age

    def clean(self):
        if self.get_age() < 18:
            raise ValidationError('Возраст должен быть 18+')

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    allergies = models.TextField('Аллергии', blank=True)
    chronic_diseases = models.TextField('Хронические заболевания', blank=True)
    skin_type = models.CharField('Тип кожи', max_length=50, blank=True)

    def __str__(self):
        return f"Профиль клиента: {self.user.get_full_name()}"

    class Meta:
        verbose_name = 'Профиль клиента'
        verbose_name_plural = 'Профили клиентов'











