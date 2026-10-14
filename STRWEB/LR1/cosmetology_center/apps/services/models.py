from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField('Название категории', max_length=100)
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуг'


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField('Название услуги', max_length=200)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    duration = models.IntegerField('Длительность (мин)', default=30)
    is_active = models.BooleanField('Активна', default=True)

    def __str__(self):
        return f"{self.name} - {self.price} руб."

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'