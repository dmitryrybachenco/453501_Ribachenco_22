from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.users.models import User
from apps.services.models import Service


class PromoCode(models.Model):
    code = models.CharField('Промокод', max_length=50, unique=True)
    discount_percent = models.IntegerField('Скидка %', validators=[MinValueValidator(0), MaxValueValidator(100)])
    valid_from = models.DateTimeField('Действует с')
    valid_to = models.DateTimeField('Действует до')
    is_active = models.BooleanField('Активен', default=True)

    def __str__(self):
        return f"{self.code} - {self.discount_percent}%"

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


class Coupon(models.Model):
    coupon_code = models.CharField('Купон', max_length=50, unique=True)
    discount_amount = models.DecimalField('Сумма скидки', max_digits=10, decimal_places=2)
    valid_until = models.DateField('Действителен до')
    is_used = models.BooleanField('Использован', default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='coupons')

    def __str__(self):
        return f"{self.coupon_code} - {self.discount_amount} руб."

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES)
    text = models.TextField('Текст отзыва')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_moderated = models.BooleanField('Промодерирован', default=False)

    def __str__(self):
        return f"Отзыв от {self.user.get_full_name()} - {self.rating}/5"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']